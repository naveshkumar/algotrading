Author: Navesh Kumar
Date of Signature: 19 oct 2024

Task

ETL files from :  https://vpiimmingham.sharepoint.com/:f:/s/SharingSite/Es9dWWEnEf9OkSnH6mbzYt4BUQ5nrkJm8tjKF0GBFc7QQA.

Task Requirements

 

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