<p align="center">
  <a href="https://github.com/txt/se26f/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/se26f/blob/main/docs/lect/policies.md"><img 
      src="https://img.shields.io/badge/Policies-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="#"><img
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="#"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/zrsW8F2V9"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/se26f/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC510: Software Engineering <br>NC State, Fall '26</h1>
<img src="https://raw.githubusercontent.com/txt/se26f/refs/heads/main/etc/img/se26f.png">

# Use Cases: a Worked Example

**Links:** [Home](../../../README.md) · [Project 1a](proj1a.md) ·
[Project 1b](proj1b.md) · [Poster rules](poster.md) ·
[Prior projects](https://drive.google.com/drive/u/2/folders/1dGGQNCWC3BakD-nUZn5vPecPdm0KAhXA)

## The structure of a use case

| Part | What it says |
|---|---|
| **Name** | Verb + noun, actor's goal ("Place order") |
| **Primary actor** | Who wants the goal |
| **Stakeholders & interests** | Who else cares, what they want |
| **Preconditions** | Must be true before start |
| **Trigger** | Event that kicks it off |
| **Main success scenario** | Numbered steps, actor ↔ system, happy path only |
| **Extensions** | Numbered variations/failures, keyed to steps ("3a: card declined → ...") |
| **Postconditions** | Guaranteed true on success |

Notes:

- The main scenario stays clean — no ifs. All branching lives in the extensions. That separation is the whole trick.
- Extensions are where the requirements hide. You will find more real requirements there than in the happy path.
- Name from the actor's goal, not the system's function ("Track delivery," not "Display status screen").
- Steps say *what*, not *how* — no UI widgets, no database talk.

---

## UC1: Place order

| Part | Content |
|---|---|
| **Name** | Place order |
| **Primary actor** | Customer |
| **Stakeholders & interests** | Customer: fast, correct meal. Restaurant: accurate order, payment. Platform: commission, fraud avoidance. |
| **Preconditions** | Customer registered and logged in; at least one restaurant open and in range. |
| **Trigger** | Customer decides to order food. |
| **Main success scenario** | 1. Customer browses nearby restaurants. 2. Customer selects restaurant and views menu. 3. Customer adds items to cart. 4. Customer confirms delivery address and pays. 5. System charges payment and creates the order. 6. System confirms order with estimated delivery time. |
| **Extensions** | 3a: Item out of stock → system hides or marks it; customer picks another. 4a: Address outside delivery zone → system rejects, asks for new address. 5a: Payment declined → system asks for another payment method. |
| **Postconditions** | Order exists, paid for, and is queued for the restaurant; customer has confirmation and ETA. |

## UC2: Track delivery

| Part | Content |
|---|---|
| **Name** | Track delivery |
| **Primary actor** | Customer |
| **Stakeholders & interests** | Customer: know when food arrives. Support: fewer "where is my order?" calls. |
| **Preconditions** | Customer has an active order. |
| **Trigger** | Customer opens the order status page. |
| **Main success scenario** | 1. Customer opens active order. 2. System shows current status (accepted → cooking → picked up → arriving). 3. System shows courier position and updated ETA. 4. Customer watches until delivery is marked complete. |
| **Extensions** | 2a: Order delayed past ETA → system notifies customer with new ETA. 3a: Courier GPS unavailable → system shows status only, no map. |
| **Postconditions** | Customer has seen current, truthful order status. |

## UC3: Fulfill order

| Part | Content |
|---|---|
| **Name** | Fulfill order |
| **Primary actor** | Restaurant |
| **Stakeholders & interests** | Restaurant: manageable queue, no wasted food. Customer: order accepted quickly. Platform: low rejection rate. |
| **Preconditions** | Restaurant is open and logged into the order terminal. |
| **Trigger** | New order arrives from the platform. |
| **Main success scenario** | 1. System presents new order to restaurant. 2. Restaurant accepts the order. 3. System notifies customer and requests a courier. 4. Restaurant prepares the food. 5. Restaurant marks the order ready for pickup. |
| **Extensions** | 2a: Restaurant rejects (too busy, out of stock) → system refunds customer and apologizes. 2b: No response within N minutes → system auto-cancels and refunds. |
| **Postconditions** | Order is cooked and waiting for courier pickup; customer informed. |

## UC4: Deliver order

| Part | Content |
|---|---|
| **Name** | Deliver order |
| **Primary actor** | Courier |
| **Stakeholders & interests** | Courier: fair pay, efficient route. Customer: hot food, on time. Restaurant: prompt pickup. |
| **Preconditions** | Courier is online and near the restaurant; order is ready or nearly ready. |
| **Trigger** | System offers the delivery job to the courier. |
| **Main success scenario** | 1. Courier accepts the job. 2. System provides route to restaurant. 3. Courier picks up the order and confirms pickup. 4. System provides route to customer. 5. Courier hands over the food and confirms delivery. 6. System pays the courier and closes the order. |
| **Extensions** | 1a: Courier declines → system offers job to next courier. 5a: Customer unreachable → courier waits N minutes, then follows drop-off/return policy. |
| **Postconditions** | Customer has the food; courier is paid; order closed. |

## UC5: Rate and refund

| Part | Content |
|---|---|
| **Name** | Rate and refund |
| **Primary actor** | Customer |
| **Stakeholders & interests** | Customer: redress for bad experience. Restaurant/courier: fair ratings. Platform: retain trust, limit refund abuse. |
| **Preconditions** | Order was delivered (or marked delivered). |
| **Trigger** | Customer opens the completed order to review or complain. |
| **Main success scenario** | 1. Customer rates meal and courier. 2. System records ratings against restaurant and courier. 3. Customer thanked; ratings feed public averages. |
| **Extensions** | 1a: Customer reports a problem (missing/cold/wrong item) → support reviews evidence → refund or credit issued. 1b: Repeated refund claims from same account → system flags for fraud review. |
| **Postconditions** | Ratings recorded; any valid complaint resolved with refund/credit. |
