#include <iostream>
#include <sys/resource.h>
#include <sys/time.h>
#include <math.h>
#include <stdlib.h>

#include <vector>
#include <algorithm>
#include <fstream>
using namespace std;

enum Owner {
    OWNER_NONE   = -1,
    OWNER_ME     = 0,
    OWNER_ALLY   = 1,
    OWNER_ENEMY  = 2
};

struct Flight {
    int from;
    int to;
    Owner owner;
    int shipcount;
    int turns;
};

struct Star {
    int x, y;
    int richness;
    Owner owner;
    int turns;
    int shipcount;
    std::vector<int> links;
    std::vector<Flight> inFlights;  // incoming flights
    std::vector<Flight> outFlights; // outgoeing flights
    bool valid; // valid intel?
    float distance; // distance from current my star (for sorting)
    
    Star(int _x, int _y) : x(_x), y(_y), valid(false) { }
};

std::vector<Star> stars;
std::vector<int> myStars;


float Distance(int id1, int id2)
{
    const Star &s1 = stars[id1];
    const Star &s2 = stars[id2];
    return (s1.x-s2.x)*(s1.x-s2.x) + (s1.y-s2.y)*(s1.y-s2.y);
}
bool IsLinked(int id1, int id2)
{
    const Star &s = stars[id1];
    for(int i = 0; i < s.links.size(); ++i)
    {
        if(s.links[i] == id2) return true;
    }
    return false;
}

bool IsFlyingTo(int to, Owner owner)
{
    const Star &s = stars[to];
    for(int i = 0; i < s.inFlights.size(); ++i)
    {
        if(s.inFlights[i].owner == owner) return true;
    } 
    return false;
}

bool IsFlyingFromTo(int from, int to, Owner owner)
{
    const Star &s = stars[from];
    for(int i = 0; i < s.outFlights.size(); ++i)
    {
        if(s.outFlights[i].owner == owner && s.outFlights[i].to == to) return true;
    } 
    return false;
}

bool TeamIsFlyingTo(int to)
{
    return IsFlyingTo(to, OWNER_ALLY) || IsFlyingTo(to, OWNER_ME);
}

bool CandidateDistance(int i, int j)
{
    return stars[i].distance < stars[j].distance;
}

int CaptureTurns(int to)
{
    const Star &star = stars[to];
    int turns = 65536;
    for(int i = 0; i < star.inFlights.size(); ++i)
    {
        if(star.inFlights[i].shipcount >= 6)
        {
            if(star.inFlights[i].turns < turns) turns = star.inFlights[i].turns;
        }
    }
    return turns;
}

void Fly(int from, int to, int ships, Star &fromStar, Star &toStar)
{
    cout << "fly " << from << " " << to << " " << ships << endl;
    fromStar.shipcount -= ships;
    
    // new flight
    Flight flight;
    flight.from = from;
    flight.to = to;
    flight.shipcount = ships;
    flight.owner = OWNER_ME;
    flight.turns = int(ceilf(sqrtf(Distance(from, to)) / 10));
    fromStar.outFlights.push_back(flight);
    toStar.inFlights.push_back(flight);
}


int main() {
  std::ios::sync_with_stdio(false);

  // Read initial galaxy configuration.
  string dummy;
  cin >> dummy;
  for (int i = 0; i < 90; i++) {
    int x, y;
    cin >> x >> y;
    stars.push_back(Star(x, y));
  }

  while (true) 
  {
    // invalidate intel
    for(std::vector<Star>::iterator it = stars.begin(); it != stars.end(); ++it)
    {
        Star &star = *it;
        star.links.clear();
        star.inFlights.clear();
        star.outFlights.clear();
        star.valid = false;
    }
    myStars.clear();
    
    while (true) 
    {
      if (!cin) return 0;
      string cmd;
      cin >> cmd;
      if (cmd == "star") 
      {
        int id, richness, owner, shipcount, turns;
        cin >> id >> richness >> owner >> shipcount >> turns;
        stars[id].richness = richness;
        stars[id].owner = Owner(owner);
        stars[id].shipcount = shipcount;
        stars[id].turns = turns;
        stars[id].valid = true;
        if(owner == OWNER_ME) myStars.push_back(id);
      } 
      else if (cmd == "link") {
        int from, to;
        cin >> from >> to;
        stars[from].links.push_back(to);
        stars[to].links.push_back(from);
      } 
      else if (cmd == "flight") {
        int from, to, owner, shipcount, turns;
        cin >> from >> to >> shipcount >> owner >> turns;
        Flight flight;
        flight.from = from;
        flight.to = to;
        flight.shipcount = shipcount;
        flight.owner = Owner(owner);
        flight.turns = turns;
        stars[from].outFlights.push_back(flight);
        stars[to].inFlights.push_back(flight);
      } 
      else if (cmd == "done") 
      {
        break;
      }
    }

    // sorted candidates by distance
    std::vector<int> candidates;
    for(int i = 0; i < stars.size(); ++i) candidates.push_back(i);
    
    // for each controlled star
    for(std::vector<int>::const_iterator it = myStars.begin(); it != myStars.end(); ++it)
    {
        // current star
        int from = *it;
        Star &fromStar = stars[from];
        if(fromStar.shipcount <= 0) continue; // skip empty stars
        
        // compute distances -> sort candidates
        for(int i = 0; i < stars.size(); ++i)
        {
            stars[i].distance = Distance(from, i);
        }
        std::sort(candidates.begin(), candidates.end(), CandidateDistance);
        
        // foreach candidate
        int lastCandidate = 0;
        for(int i = 0; i < candidates.size(); ++i)
        {
            int to = candidates[i];
            if(to == from) continue; // skip myself
            Star &toStar = stars[to];

            if(toStar.distance > 3600 || fromStar.shipcount <= 0) break; // too far or no ships availabe -> end
            lastCandidate = i;

            if(!toStar.valid) continue; // skip not valid intel
            
            if(toStar.owner == OWNER_NONE && fromStar.shipcount >= 6) // priority -> conquare free stars
            {
                int enemyTurns = CaptureTurns(to);
                int myTurns = (int)ceilf(sqrtf(toStar.distance) / 10);
                if(myTurns < enemyTurns)
                    Fly(from, to, 6, fromStar, toStar);
            }
            else if(toStar.owner == OWNER_ENEMY && fromStar.shipcount >= 15 + toStar.shipcount) // attack
            {
                int count = /*15 + toStar.shipcount*/fromStar.shipcount;
                Fly(from, to, count, fromStar, toStar);
            }           
            else if(toStar.owner == OWNER_ALLY && !IsLinked(from, to) && !IsFlyingFromTo(to, from, OWNER_ALLY) && !IsFlyingFromTo(from, to, OWNER_ME)) // link probe
            {
                Fly(from, to, 1, fromStar, toStar);
            }
        }
    
        // still enough ships?    
        if(fromStar.shipcount > 0)
        {
            // find nearest enemy
            for(int i = 0; i < candidates.size(); ++i)
            {
                const int toEn = candidates[i];
                const float fromToEnDist = Distance(from, toEn);
                const Star &toStarEn = stars[toEn];
                if(toStarEn.valid && toStarEn.owner == OWNER_ENEMY && !IsFlyingFromTo(from, toEn, OWNER_ME)) 
                {
                    // find alley candidate that is near then me
                    int toBest = -1;
                    float bestToEn = 1e30f;
                    for(int j = 0; j <= lastCandidate; ++j)
                    {
                        int to = candidates[j];
                        const Star &toStar = stars[to];
                        if(!toStar.valid || from == to) continue;
                        
                        if(toStar.owner == OWNER_ME || toStar.owner == OWNER_ALLY)
                        {
                            float to2en = Distance(to, toEn);
                            if(to2en < fromToEnDist && to2en < bestToEn) 
                            {
                                bestToEn = to2en;
                                toBest = to;
                            }
                        }
                    }
                    if(toBest >= 0)
                    {
                        Star &toStar = stars[toBest];
                        if(fromStar.shipcount > 6 || Distance(from, toEn) > 1600)
                            Fly(from, toBest, fromStar.shipcount, fromStar, toStar);
                    }
                    break;
                }
            }
        }
    } // for all controlled stars
    
    cout << "done" << endl;
  }
}
