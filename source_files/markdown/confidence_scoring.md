# Scoring System

## Definition
Once all data is collected, a logistic regression model is applied to derive a single score.

## Steps
1. Collect `observed_y(t)` for all metrics.
2. Calculate the index score: a weighted combination of all variables using logistic regression.
3. Derive the beta (correlation coefficient) for each variable relative to the index.
4. Derive the final score.

## Output
Final health score and contribution of each variable.

## Formula for Deriving Beta

The formula for deriving beta, which measures the sensitivity of a variable relative to an index, is given by:

\[
\beta = \frac{\text{cov}(x, i)}{\text{var}(i)}
\]

Where:
- \( x \) is the variable of interest.
- \( i \) is the index (e.g., overall score or market index).
- \( \text{cov}(x, i) \) is the covariance between the variable \( x \) and the index \( i \).
- \( \text{var}(i) \) is the variance of the index \( i \).

### Step-by-Step Calculation
1. **Calculate the mean of \( x \) and \( i \):**
   \[
   \bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
   \]
   \[
   \bar{i} = \frac{1}{n} \sum_{i=1}^{n} i_i
   \]

2. **Calculate covariance \( \text{cov}(x, i) \):**
   \[
   \text{cov}(x, i) = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x}) \times (i_i - \bar{i})
   \]

3. **Calculate variance \( \text{var}(i) \):**
   \[
   \text{var}(i) = \frac{1}{n-1} \sum_{i=1}^{n} (i_i - \bar{i})^2
   \]

4. **Calculate beta \( \beta \):**
   \[
   \beta = \frac{\text{cov}(x, i)}{\text{var}(i)}
   \]

This beta value will indicate how much the variable \( x \) moves relative to changes in the index \( i \). A beta greater than 1 means the variable is more volatile than the index, while a beta less than 1 means it is less volatile. A beta of 1 indicates that the variable moves in tandem with the index.

## Correlation Coefficient \( \xi \)

The new correlation coefficient, denoted as \( \xi \) (pronounced “ksaai”), differs from traditional measures like Pearson’s \( r \) by focusing on how much one variable is a function of another, rather than simply measuring a linear relationship between them. It is particularly useful when relationships between variables are non-linear or complex.

### How \( \xi \) Works:
1. **Sorting:** The data points are first sorted based on one variable (let’s say \( x \)).
2. **Ranking:** After sorting, the values of the second variable (y) are ranked according to their order in \( x \).
3. **Calculate \( \xi \):** The difference between consecutive ranks of \( y \) is used to calculate \( \xi \), capturing how closely \( y \) follows \( x \) in a potentially non-linear fashion. If the difference between consecutive ranks is minimal, it implies a stronger relationship, resulting in a higher \( \xi \) value.

### Example
Imagine you have two variables: \( x = [1, 2, 3, 4] \) and \( y = [2, 4, 9, 16] \). The relationship between \( x \) and \( y \) is clearly non-linear (y is x squared).

#### Steps to Calculate \( \xi \):
1. **Sort the data:**
   - The data is already sorted as \( x = [1, 2, 3, 4] \) and \( y = [2, 4, 9, 16] \).

2. **Rank \( y \):**
   - Rank the values of \( y \) based on \( x \). Here, since \( y \) is increasing, the ranks are \( r = [1, 2, 3, 4] \).

3. **Calculate \( \xi \):**
   - Compute the differences between consecutive ranks. Since the ranks are evenly spaced (i.e., 1, 2, 3, 4), the difference between consecutive ranks is minimal.
   - The \( \xi \) coefficient would then be close to 1, indicating a strong relationship between \( x \) and \( y \).

### Key Differences from Pearson’s \( r \):
- **Non-linearity:** While Pearson’s \( r \) would detect no strong linear relationship (it would likely show a weak correlation), \( \xi \) captures the non-linear relationship effectively.
- **Robustness:** \( \xi \) is more robust to different types of relationships and doesn’t require assumptions about the data distribution.

# Confidence Score Calculation

## Overview

The confidence score is an approximation of a nonlinear relationship between the number of tickets an agent has handled and the consistency (or variability) in sentiment scores for those tickets. The score is designed to assess the reliability of the average sentiment score for each agent, with a higher confidence score indicating more reliability.

This confidence score formula is not equivalent to more formal correlation measures like Pearson’s correlation coefficient (ρ) or the nonlinear ξ coefficient. Instead, it focuses on providing a simplified measure of how confident we are in the sentiment score based on two factors:

1.	The number of tickets the agent has handled.
2.	The variability (standard deviation) of the sentiment scores for those tickets.

## Confidence Score Formula

The confidence score for an agent is calculated as:

```
\text{Confidence Score} = \frac{1}{1 + \frac{\sigma_{\text{sentiment}}}{\text{tickets}}}

Where:

\sigma_{\text{sentiment}}  is the standard deviation of the sentiment scores.
\text{tickets}  is the total number of tickets the agent has handled.
```

This formula increases the confidence score as the number of tickets increases or the variability decreases. It’s non-linear, meaning that as the number of tickets grows, the score approaches 1 (high confidence), but with diminishing returns. Similarly, as variability increases, the confidence score decreases.

## Relationship to Pearson’s Correlation and ξ

### Pearson’s Correlation (ρ)

Pearson’s correlation coefficient is used to measure the linear relationship between two variables. It tells us how well one variable can predict another. In contrast, the confidence score is not about measuring the relationship between variables but about evaluating the reliability of a single variable (the average sentiment score). It’s more concerned with how consistent an agent’s sentiment scores are across multiple tickets.

### ξ Coefficient (Nonlinear Correlation)

The ξ coefficient measures nonlinear correlations between variables. While the confidence score shares some characteristics of nonlinearity, it is not a formal correlation measure. The confidence score is more of an approximation for reliability, where we increase confidence as the number of data points grows and decrease confidence with greater variability.

Unlike ξ, which looks at the strength of relationships between variables in nonlinear ways, the confidence score is a practical, simplified measure focused on how much data (tickets) and how consistent the results (sentiment) are.

### Use Case

The confidence score helps prioritize agents with more ticket data and lower variability in sentiment. It is useful for:

+ Identifying agents whose average sentiment score is more reliable.
q+ Prioritizing agents with a larger number of consistent tickets over those with fewer or more variable results.

The score is not intended to explore relationships between variables like Pearson’s or ξ but instead provides a rough estimate of the reliability of the sentiment data.

SQL Query Example

```
CREATE OR REPLACE TABLE `project.dataset.confidence_score` AS
WITH agent_stats AS (
  -- Step 1: Calculate agent-level metrics including standard deviation of sentiment
  SELECT 
    agent_name,
    COUNT(Ticket_ID) AS tickets,  -- Total number of tickets
    ROUND(AVG(Sentiment), 1) AS avg_sentiment,  -- Avg sentiment score
    STDDEV(Sentiment) AS stddev_sentiment  -- Variability in sentiment score
  FROM `project.dataset.tickets`
  GROUP BY agent
),

-- Step 2: Calculate Confidence Score for each agent
confidence_calc AS (
  SELECT
    agent_name,
    tickets,
    avg_sentiment_integer,
    stddev_sentiment,
    -- Confidence score formula: more tickets + less variability -> higher confidence
    CASE 
      WHEN stddev_sentiment IS NULL THEN 1  -- If no variability, high confidence
      ELSE ROUND(1 / (1 + (stddev_sentiment / tickets)), 2)  -- Confidence score formula
    END AS confidence_score  -- Higher tickets and lower stddev lead to higher confidence
  FROM agent_stats
)

-- Step 3: Select final output
SELECT 
  agent_name,
  tickets,
  avg_sentiment_integer,
  confidence_score
FROM confidence_calc
ORDER BY confidence_score DESC, tickets DESC;
```

This query calculates the confidence score for each agent and stores it in a table called confidence_score. The score is based on the agent’s sentiment score variability and the number of tickets they have handled, giving a higher confidence score to agents with more consistent data.
