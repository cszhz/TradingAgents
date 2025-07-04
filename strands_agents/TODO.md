
# TODO List for Strands SDK Implementation

This document outlines the tasks required to re-implement the trading agents using the Strands Agent SDK.

## 1. Project Setup

*   [x] Install the `strands-agents` and `strands-agents-tools` packages.
*   [x] Create a new directory `strands_agents` to house the new implementation.

## 2. Tool Refactoring

*   [x] Refactor the `Toolkit` class and its methods to be compatible with the Strands SDK.
*   [x] Each tool in the `Toolkit` should be a Python function decorated with the `@tool` decorator.
*   [x] Ensure all data-fetching functions in the `dataflows` directory are compatible with the Strands SDK's tool definition.

## 3. Agent Implementation

*   [x] Implement the `FundamentalsAnalyst` as a Strands `Agent`.
*   [x] Implement the `MarketAnalyst` as a Strands `Agent`.
*   [x] Implement the `NewsAnalyst` as a Strands `Agent`.
*   [x] Implement the `SocialMediaAnalyst` as a Strands `Agent`.
*   [x] Implement the `ResearchManager` as a Strands `Agent`.
*   [x] Implement the `RiskManager` as a Strands `Agent`.
*   [x] Implement the `BearResearcher` as a Strands `Agent`.
*   [x] Implement the `BullResearcher` as a Strands `Agent`.
*   [x] Implement the `AggresiveDebator` as a Strands `Agent`.
*   [x] Implement the `ConservativeDebator` as a Strands `Agent`.
*   [x] Implement the `NeutralDebator` as a Strands `Agent`.
*   [x] Implement the `Trader` as a Strands `Agent`.

## 4. Workflow Orchestration

*   [x] Replace the custom graph implementation in the `tradingagents/graph` directory with the Strands SDK's multi-agent collaboration and workflow orchestration features.
*   [x] Replace the custom `TypedDict` state management with the Strands state management system.

## 5. Memory Integration

*   [x] Create a custom tool that allows the Strands agents to interact with the `FinancialSituationMemory`.

## 6. Testing

*   [ ] Write unit tests for the new Strands agents and tools.
*   [ ] Write integration tests to ensure the entire workflow functions as expected.

## 7. Documentation

*   [ ] Update the project documentation to reflect the new implementation.
