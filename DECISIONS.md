# Design and Architectural Decisions

This document outlines the key technical and architectural decisions made during the development of the BITA Mini Backtest API project. It also highlights alternatives that were considered and why certain approaches were ultimately chosen or discarded.

---

## Code Structure Decisions

### Modularized Application

- **Separation of Concerns**:  
  Divided the project into distinct modules (`api.py`, `models.py`, `backtest_engine.py`, `utils.py`, `data_loader.py`) to isolate:
  - API routing and request handling
  - Core business logic (backtesting)
  - Data loading operations
  - Utility functions
- **Why**: 
  - Improves readability and maintainability.
  - Allows for faster debugging and testing.
  - Facilitates future scalability — new features can be added in new files without disrupting existing logic.

### Lightweight Core Engine

- **Design**: `backtest_engine.py` focuses purely on business logic without any API framework dependencies.
- **Why**:
  - Keeps core logic portable and testable independently.
  - Allows reusability if needed outside FastAPI context.

---

## Technology Choices

### FastAPI for the API Layer

- **Why**:
  - Built-in async support and automatic documentation with Swagger UI.
  - Extremely lightweight and fast compared to Django/Flask for microservices.

### Pandas for Data Handling

- **Why**:
  - Native support for time-series data.
  - Fast vectorized operations.
  - Well-integrated with Parquet file format via PyArrow.

### Parquet Files as Data Source

- **Why**:
  - Columnar storage format — highly space efficient for large tabular data.
  - Very fast read times compared to CSVs, especially when only specific columns are needed.
- **Memory Advantage**:
  - Parquet minimizes RAM usage by allowing selective reading and compression.

---

## Optimization Strategy

- **Updated Approach**:
  - Instead of using external solvers like `scipy.optimize.linprog`, we implemented a **manual heuristic optimization** approach to determine portfolio weights.
  - **Method**:
    - Assign minimum (lower bound) weight to all selected securities.
    - Distribute remaining weight preferentially to higher-value securities, while respecting the upper bounds.
    - Ensure final weights sum to exactly 1.
- **Why**:
  - Matches the project guidelines to avoid external optimization libraries.
  - Keeps the system lightweight, easy to debug, and avoids solver-related dependencies.
  - The heuristic still respects all constraints (bounds, full investment).

- **Trade-offs**:
  - True mathematical optimality (global maximum) is not always guaranteed.
  - However, the heuristic provides a reasonable approximation while maintaining simplicity and interpretability.

---

## Memory and Space Complexity Decisions

- **Memory Conscious Design**:
  - Only **load one field (one Parquet file)** per request, not all fields at once — avoids unnecessary memory bloat.
  - Work at **row level (single date)** rather than loading the full historical time series into memory at once.
- **Efficiency**:
  - Filtering and weighting operations are fully vectorized using Pandas — O(N) complexity where possible.
  - No use of heavy in-memory caching unless explicitly needed, keeping the application lightweight for API-first usage.

---

## Discarded Alternatives and Why

### 1. Full In-Memory Dataset Loading

- **Discarded**:
  - Initially considered loading the entire dataset into memory for faster access.
- **Why Not**:
  - Not scalable when datasets grow (e.g., thousands of securities × years of history).
  - Increases memory consumption unnecessarily.

### 2. Pre-computing All Rebalancing Dates and Storing

- **Discarded**:
  - Thought about precomputing all possible portfolio rebalancings at startup.
- **Why Not**:
  - Limits flexibility for custom dates.
  - Would make the service less dynamic for user-specific inputs.

### 3. Using External Optimization Solvers

- **Discarded**:
  - Initially used `scipy.optimize.linprog` to solve the portfolio optimization accurately.
- **Why Not**:
  - Based on project guidelines, reliance on external solvers was not allowed.
  - Manual heuristic optimization was preferred to keep the solution lightweight, understandable, and free of external mathematical solvers.

---

## Future-Proofing

- **Scalable**:  
  Codebase can handle larger datasets simply by switching data loaders or parallelizing date-wise operations.
- **Extensible**:  
  Easy to add new calendar rules, new filtering methods, or new weighting strategies without breaking existing APIs.
- **Production-Ready Foundations**:  
  Designed with clean error handling, input validation, modular architecture, and lightweight dependencies to ease transition to real-world deployment environments.

---

## Additional Enhancements (Beyond Project Scope)

To further enhance the robustness, observability, and production-readiness of the API, the following features were independently added:

### 1. `/health` Endpoint

- **Purpose**: Simple health check API endpoint to monitor service uptime and basic availability.
- **Reason**: Common industry best practice for microservices; allows easy integration with monitoring systems or load balancers.

### 2. Request Logging Middleware

- **Purpose**: Middleware that logs every incoming HTTP request's method and path.
- **Reason**: Improves observability and debugging capability; crucial for tracing API activity in production environments.

### 3. API Versioning

- **Purpose**: Added explicit versioning (`1.0.0`) to the FastAPI application metadata.
- **Reason**: Prepares the API for future backward-compatible upgrades and makes it easier to manage evolving API changes professionally.

---

# Final Thought

The overall goal was to build a fast, scalable, memory-efficient backtesting engine while maintaining codebase simplicity and extensibility.  
Every decision was made keeping in mind practical considerations of **memory efficiency**, **simplicity**, **developer ergonomics**, and **real-world performance**.
