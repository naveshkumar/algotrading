Author: Navesh Kumar
Date of Signature: 19 oct 2024

Task

ETL files from :  https://vpiimmingham.sharepoint.com/:f:/s/SharingSite/Es9dWWEnEf9OkSnH6mbzYt4BUQ5nrkJm8tjKF0GBFc7QQA.

Task Requirements

##### Question #### [See Instructions for using algo framework below]
 

You are asked to perform the following:

 

    Perform simple exploratory data analysis on the provided orderbook snapshots with reproducible code, and document your observations of anything interesting or unusual.
    Propose and implement a simple intraday power trading strategy in code, using the data provided.
        The sophistication or profitability of your strategy is not important for this task.
        Your proposed strategy can be asset based e.g. CCGT, BESS, but is not required to be so.
    Create a reproducible code pipeline that performs back-testing when given a) the orderbook dataset, and b) an intraday power trading strategy:

        The back-testing pipeline must produce statistically valid and commercially relevant results, for the purpose of providing conclusive evidence for/against deploying the strategy.
        The pipeline should work for more than just your trading strategy; you may wish to implement a generic strategy class to facilitate then demonstrate this.
        The pipeline must allow data from a user specifiable unseen dataset to be used, and to produce valid out-of-sample results; you can assume the unseen dataset will have the same format as the historical data already provided.

    Create a short presentation deck with the back-tested results, produced by your pipeline on your proposed strategy:
        Clearly demonstrate why/why not your proposed strategy should be allowed to be deployed for live trading.
        The intended audience is a mix of traders and quants, who will query you to explain your methodology and results.
        A robust, well evidenced recommendation against deployment is equally valued as one recommending for it, though you may then wish to indicate what quantitatively and qualitatively needs to be improved, in a hypothetical next version, for the recommendation to become positive.
        6 slides or fewer recommended, but you may optionally include a small number of appendix slides as supporting evidence.

 

Additional Criteria

 

    Python is strongly recommended. However if another language e.g. R must be used, you will be asked to clearly demonstrate how its equivalent can be implemented in Python. You may also find Jupyter Notebooks (or equivalent) useful for analysis visualisations.
    All code and results must be reproducible. You must provide clear, unambiguous instructions to rerun your code error-free in an equivalent environment, such that it can produce identical results to your own.
    We do not encourage including additional datasets other than what we provided, but if you choose to incorporate any, you must then:
        Include a reproducible ingestion method in code
        Provide a copy of the data in your task return to reproduce all results

Any such additional dataset must be publicly accessible through the internet, from an open provider, without cost involved.



Class Overview

The momentumalgo class is a subclass of the general_algo_framework and implements a specific trading algorithm based on market momentum. The class monitors bid and offer prices for a financial product and executes trades based on the observed changes in price momentum.
Methods
1. DataSetup(self)

    Purpose: This method sets up the data and context for the algorithm to operate. It defines where the input data is stored and the location for output.
    Parameters: None.
    Returns: None.
    Actions:
        Sets the algorithm context to "Backtest".
        Specifies the file path to input data (market snapshots).
        Specifies the output location to store results.

Example:

python

algo_instance.DataSetup()

2. TimeContext(self)

    Purpose: This method sets the time frame for the algorithm’s observation and defines the time range for product analysis.
    Parameters: None.
    Returns: None.
    Actions:
        Sets the start and end times for the algorithm's observation period.
        Defines the observation window for products before their gate closure.
        Specifies which products (e.g., Quarter Hour products) will be traded and their internal IDs.

Example:

python

algo_instance.TimeContext()

3. AlgoMemory(self)

    Purpose: Initializes and stores the state of the algorithm's memory, which helps in controlling the algorithm’s flow, especially for opening and closing trades based on momentum.
    Parameters: None.
    Returns: None.
    Actions:
        Initializes the internal algorithm memory to store the calibration moments (t0 and t1), trade open/close states, and direction for closing trades.

Example:

python

algo_instance.AlgoMemory()

4. Algorithm(self, current_product, onData, GC, current_nop)

    Purpose: This method is the core of the trading strategy. It calculates momentum based on the current bid and offer prices and executes buy or sell trades depending on the momentum direction.
    Parameters:
        current_product: The financial product being traded.
        onData: DataFrame containing real-time bid, offer, and volume data.
        GC: Gate Closure time for the product.
        current_nop: Current net open position.
    Returns: None.
    Actions:
        The algorithm first determines the best current bid and offer prices and volumes at the highest priority levels.
        Trades are triggered based on the price momentum, with conditions for when to open and close trades.
        The algorithm checks for specific time intervals relative to the gate closure and stores trade results in the PnLBook.
        It opens a trade if there is a momentum and closes it based on further price movements.

Example:

python

algo_instance.Algorithm(current_product, onData, GC, current_nop)

How to Use the momentumalgo Class
Step 1: Import and Initialize

First, ensure you have imported the necessary general_algo_framework class and Pandas. Then, initialize an instance of the momentumalgo class.

python

from momentumalgo import momentumalgo

# Create an instance of the momentumalgo class
algo_instance = momentumalgo()

Step 2: Set Up Data and Time Context

You need to set up the data locations and define the time context for the algorithm to operate within.

python

# Setup Data locations
algo_instance.DataSetup()

# Define the time context
algo_instance.TimeContext()

Step 3: Initialize Algorithm Memory

Initialize the memory to store the algorithm's internal state during the trade execution.

python

algo_instance.AlgoMemory()

Step 4: Run the Algorithm

The core logic of the algorithm runs by passing in the necessary arguments, including the current product, onData (market data), gate closure time, and net open position.

python

# Assuming you have the necessary data for 'current_product', 'onData', 'GC', and 'current_nop'
algo_instance.Algorithm(current_product, onData, GC, current_nop)

Step 5: Review Results

The results of the trades are stored in the PnLBook (Profit and Loss Book) attribute of the class, which you can review.

python

# View the PnLBook after running the algorithm
print(algo_instance.PnLBook)

Additional Information

    Trade Opening and Closing Logic:
        The algorithm compares bid and offer prices at specific time intervals relative to the gate closure (e.g., 60-65 minutes and 30-35 minutes).
        The momentum between the two calibration moments (t0 and t1) determines whether to open a "BUY" or "SELL" trade.

    Internal Product IDs:
        The products are referred to using internal IDs, which are stored in a dictionary during the TimeContext() setup.


#### how to run this code:
# configure the command trading algo subclass 
# the algorithm part needs to be treated as a apply style function on a growing dataframe that looks like the snapshot of the trading session from POS to POE
# save the code
# run the command line layer

# please reach out to naveshkumar92@gmail.com for queries. This function does not have python documentation
