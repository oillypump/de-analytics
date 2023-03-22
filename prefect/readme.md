If you want to start running flows on a schedule, via the API, from the Prefect UI, or on distributed infrastructure, you'll need to understand a few additional concepts and perform some configuration.

1. Start a local Prefect server with prefect server start or create a free Prefect Cloud account.

**prefect server ini adalah UI-nya**

2. Set PREFECT_API_URL to enable communication between your execution environment and the Prefect server or Prefect Cloud API.

**prefect api url ini utk communicate antara prefect server dengan code yang kita running**

3. Configure storage to persist flow and task data.
4. Create a deployment for a flow, giving the API metadata about where your flow's code is stored and how your flow should be run.
5. Start an agent that can execute scheduled or ad-hoc flow runs from your deployments.

**agent ini running yang digunakan utk bisa menangkap task yang akan di execute atau by schedule**