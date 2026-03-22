# Module Dependency Graph

No circular dependencies detected — every module can be changed in isolation
by working from right to left in the diagram.

**Safe change order (least to most impact):**

1. `stdlib` / `third-party` — not owned by this project
2. `app.py` — only dependency is loguru + sys; nothing internal imports it except `cli.py`
3. `cli.py` — depends on `app.py`; changing it only affects `__main__.py` and the tests
4. `__main__.py` — thin entry point, safe to change freely
5. `serve_docs.py` — fully isolated, no internal imports
6. `conftest.py` — test-only, no production imports

```mermaid
flowchart LR
    subgraph pkg["📦 second_brain/"]
        direction TB
        main["__main__.py"]
        cli["cli.py"]
        app["app.py"]
    end

    subgraph tests["🧪 tests/"]
        direction TB
        test_app["test_app.py"]
        conftest["conftest.py"]
    end

    subgraph scripts["📜 scripts/"]
        serve_docs["serve_docs.py"]
    end

    subgraph third_party["Third-party"]
        direction TB
        loguru["loguru"]
        click["click"]
        pytest["pytest"]
    end

    subgraph stdlib["stdlib"]
        direction TB
        sys["sys"]
        os_dt_path["os · datetime · Path"]
        subprocess["subprocess"]
    end

    main       --> cli
    cli        --> app
    cli        --> click
    cli        --> loguru
    cli        --> os_dt_path
    app        --> loguru
    app        --> sys
    test_app   --> cli
    test_app   --> click
    conftest   --> pytest
    serve_docs --> sys
    serve_docs --> subprocess
```

> No red nodes — zero circular dependencies found.
