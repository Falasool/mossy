<div align="center">
  <h1>Mossy</h1>
  <h2>❤️ Yet another interplanetary microblogging platform with python</h2>

  ![GitHub License](https://img.shields.io/github/license/mattholy/mossy)
  ![GitHub Release](https://img.shields.io/github/v/release/mattholy/mossy)
  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/mattholy/mossy)
  ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/mattholy/mossy)
  ![GitHub last commit](https://img.shields.io/github/last-commit/mattholy/mossy)
  [![codecov](https://codecov.io/gh/mattholy/mossy/graph/badge.svg?token=4SJGE2QAOA)](https://codecov.io/gh/mattholy/mossy)

  [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmattholy%2Fmossy.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmattholy%2Fmossy?ref=badge_small)

----
Read this in other languages:

[简体中文](docs/readme.zh-cn.md) | [English](docs/readme.en-us.md) | [བོད་སྐད](docs/readme.bo-cn.md) | [বাংলা](docs/readme.bn-cn.md) | [繁體中文](docs/readme.zh-tw.md) | [हिन्दी](docs/readme.hi-cn.md) | [日本語](docs/readme.ja-cn.md) | [한국어](docs/readme.ko-cn.md)

</div>

<div>

# What is Mossy



Mossy is a interplanetary microblogging platform of fediverse, just like [Mastodon](https://github.com/mastodon/mastodon) or [Misskey](https://github.com/misskey-dev/misskey).

Mossy operates quickly and smoothly. Thanks to its fully asynchronous architecture, it effectively utilizes your CPU and memory resources, both on the server and client sides. We are dedicated to providing you with the most seamless experience possible.

![Static Badge](https://img.shields.io/badge/Try%20it%20out-blue?style=for-the-badge)

## Why Mossy

Mossy is here to deliver an exceptional experience with cutting-edge technology.
According to that, Mossy can do much better to protect your information & personal identity
(**We don't even need your email**).

We lovingly provide:

- **Full ActivityPub support**: Yes, Mossy supports ActivityPub. Even more, all types of activities are **supported**, e.g. status, article, gallery, ask box...
- **Creator-friendly**: Mossy will be compatible with HDR photos and videos, and supports most wide color gamuts
- **High performance**: Even a small server can handel a large number of requests from fediverse
- **Flexible cluster**: Setup any new node within your cluster at your will
- **Compatible with Mastodon's APIs**: So any application developed for Mastodon can generally be used with Mossy as well (Maybe, we are tring)
- **Cluster of clusters**: Each Mossy Cluster can communicate with other Mossy Clusters, using algorithms to eliminate spam
- **Privacy**: Mossy will never collect your personal information, and will never share your data with third parties. Additionally, when everyone in the chat is using Mossy, we support end-to-end encryption to ensure your conversations are secure and worry-free.

</div>

# Getting Start

> [!IMPORTANT]
> After your server's first starts, any frontend page will redirect you to the setup interface to register and create admin details. Ensure no external access until setup is complete to avoid unauthorized use. 
> 
> **If issues arise, clear the entire database.**

A typical deployment involves placing your Mossy web services behind a load balancer (also a SSL-terminate proxy). You can deploy Mossy nodes worldwide, connecting them via a shared storage. By configuring your load balancer carefully, users can access your Mossy through the nearest access point.

> [!NOTE]
> Communication between Mossy and end users is secured with HTTPS. However, connections from Mossy to databases, message queue or load balancer may be unsafe without protective measures like TLS or VPN.

After considered things above, use the `docker-compose.yml` to deploy a single production-ready server:

```yml
WIP
```

This deployment has:

- One single Mossy all-in-one node
- Database using PostgresSQL
- Message queue using ~~Garnet~~ Redis
- Object storage using MinIO

And you need a reverse proxy or a load balancer in front of it. (Don't know how? Ask Cloudflare.)

For cluster deployment and other deploy information, please refer to [Deployment Guide](docs/deployment.md).

## Environment

> [!CAUTION]
> **Do make sure every Mossy node has the same `CLUSTER_ID`, and DO NOT change it after.**

> [!NOTE]
> If you have clusters for databases and Redis, you can probably use different database and Redis URLs for every node. Otherwise make them the same.

| Name         | Instruction                                                                                                                                                                                                                                                                                      | Default value                                                                                                     |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| DATABASE_URL | A database string. Currently support PostgresSQL only.                                                                                                                                                                                                                                           | `postgresql://username:password@localhost:5432/dbname`                                                            |
| MESSAGE_URL  | A URL for message queue. Such as Redis or Garnet.                                                                                                                                                                                                                                                | `redis://:password@localhost:6379/0`                                                                              |
| S3_URL       | A URL for s3 competitive object storage. If not provided, object will stored in database. Url format: `s3://[key_id]:[key_secret]@[endpoint]/[bucket_id]?region=[your_region]`                                                                                                                   | None                                                                                                              |
| CLUSTER_ID   | RP Source & RP of Webauthn API and also for ActivityPUB Identifier. Usually it's your domain, where your end user access your site. **Once this has been set and the server is online, DO NOT MODIFY IT. Otherwise, you may lose all users' data and cause a little chaos among the Fediverse**. | `http://localhost:5173`                                                                                           |
| LOG_LEVEL    | Logger level, support `debug`,`info` and `warning`. This only controls the log output level to console.                                                                                                                                                                                          | `info`                                                                                                            |
| SERVICE_MODE | Determine service the container runs: `web` for web services and APIs, `backgrounder` for background tasks outside the request-response cycle, `scheduler` for rapid, periodic tasks, and `all` for running everything in one container.                                                         | `all`                                                                                                             |
| WORKERS      | Number of Uvicorn and Celery workers, `2` means 2 Uvicorn workers and 2 Celery workers etc.                                                                                                                                                                                                      | Half numbers of CPU cores plus 1. For example, you have a 8 cores CPU, then the default value of this will be `5` |
| NODE_ID      | [Optional] The ID of this node. Leave unset to auto-generate. Can be any string contain no white space.                                                                                                                                                                                          | Auto-generated UUID. If anything wrong, it goes `00000000-0000-0000-0000-000000000000`                            |

## Using CDN

You may want to use CDN to accelerate access. The frontend of Mossy is a SPA, so you can deploy it separately. But should you be aware of there is a CORS issue when you use a different domain for frontend and backend.

Navigate to `frontend`, edit `.env.production`, set the correct `VITE_BASE_URL` to point to your backend server, load balancer or proxy. Then run `npm run build`. After that you can find everything you need in `frontend/dist`.

## Data Security

If yor choose to store your data locally, we would like to recommend LUKS with TPM2.

In the event of a physical breach, you can quickly destroy the decryption key to protect your data.

# Everything Else

## How Mossy Works

## Dev & Tests

<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fmattholy%2Fmossy?ref=badge_large&issueType=license" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmattholy%2Fmossy.svg?type=large&issueType=license" align="right"/></a>

> [!TIP]
> Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

Before start, you need to install:

| Name   | Version |
| ------ | ------- |
| python | 3.12    |
| poetry | 1.8.2   |
| node   | 21.7.3  |
| npm    | 10.5.0  |

Everything else will be managed by `poetry` or `npm`

### Install dependences

- Install frontend dependence: `npm run install:frontend`
- Install backend dependence: `npm run install:backend`
- Install everything: `npm run install`

### Run your development server

- Run frontend development server: `npm run dev:frontend`
- Run backend development server: `npm run dev:backend`
- Just build the frontend into backend static folder: `npm run dev:build:frontend`
- Pack it up and start a production like server: `npm run dev`
- Prepare a database for development only: `docker compose up -d`, to clean them up `docker compose down`

#### When you changed database schemas

Before you commit you change to remote.
Change your current working dir to backend (`cd backend`) and run `poetry run alembic revision --autogenerate -m "[describe your changes here]"`, then run `poetry run alembic upgrade head` to update database.

The production image will update database automatically.

### Tests

#### Unit test

- Test frontend: `npm run test:frontend`
- Test backend: `npm run test:backend`
- Test everything: `npm run test`

#### Test locally

Run `docker compose --profile dev up --build`,then navigate to [http://localhost:8000](http://localhost:8000)

# License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmattholy%2Fmossy.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmattholy%2Fmossy?ref=badge_large)

----

<div align="center">
  <img src="./docs/fedi.png" alt="Fediverse Logo" width="300"/>
</div>


