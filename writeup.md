# Week 3 – Prompting Techniques: The Support-Desk Assistant

## 1. K-shot prompting

Prompt:

```
You sort messages that customers send to our online store's help desk.
Read the message and answer with one word: billing, shipping, returns, technical or other.
Write the word in lowercase and nothing else.

Customer: My discount code was not applied and I paid the full price.
Answer: billing

Customer: The courier says my parcel was delivered but I never got it.
Answer: shipping

Customer: These headphones are too big for me, can I return them?
Answer: returns

Customer: I can't reset my password, the email never comes.
Answer: technical

Customer: Do you sell gift cards?
Answer: other
```

Sample input/output:

```
[PASS] 'My card was charged twice for order 4412.' -> got 'billing', expected 'billing'
```

What I learned: The examples gave the model variety; the more good examples we add, the better it works and the fewer mistakes it makes, because it has more correct information to follow.

## 2. Chain-of-thought

Prompt:

```
You help a support agent decide if a customer can get a refund, using the refund policy below.
Think step by step and write one short line for each check:
1. How many days ago was the item bought? Is it 30 days or less?
2. Is the item unused?
3. Is it a final-sale item?
If the customer does not mention something, treat that check as passed.
The answer is YES only if all three checks pass, otherwise it is NO.
The very last line must be exactly DECISION: YES or DECISION: NO, with nothing after it.
```

Sample input/output:

```
[PASS] 'Bought 45 days ago, unused.' -> NO, expected NO
```

What I learned: One condition can make another look true, but if the model checks every condition separately step by step, each result is not affected by the others and it reaches the right decision.

## 3. Tool calling

Prompt:

```
You are the help desk assistant of an online store.
You do not know the status of any order by yourself.
When a customer asks about an order, find the order number in their message and call get_order_status with it before you answer.
Then tell the customer the status in one short sentence.
```

Sample input/output:

```
Input: Hi, can you check on order 4412 for me?
[PASS] tool called with order_id='4412'
tool result: shipped, arriving Friday
```

What I learned: With tools we can make the model do almost anything it normally can't; we tell the agent what to do in a certain situation and it runs that tool.

## 4. RAG

Prompt:

```
You answer customer questions for an online store's help desk.
Use only the information in the Context part of the message, not anything you know from outside.
If the context is empty or does not contain the answer, reply only: Sorry, I do not know that.
Keep the answer short and use the same words as the context, for example the exact number of days.
```

Sample input/output:

```
[PASS] 'How long do I have to return an item?' -> '30 days.'
[PASS] "What's your CEO's home address?" -> 'sorry, i do not know that.'
```

What I learned: Telling the model to stay only on the given text stopped it from searching the web or making up information that isn't true, so it uses the correct text from our data, which is very important in places like government and official work.

## What I learned overall

AI is good at understanding information and connecting the user with a tool, because it uses its own LLM; our tool alone could never understand any text the user writes. But it needs help: examples so it makes fewer mistakes, step-by-step thinking so one condition doesn't affect another, tools for things it normally can't do, and a text to stay on so it doesn't make things up. When I look at these four, even by using them all together we can adapt AI to almost every topic and every field.
