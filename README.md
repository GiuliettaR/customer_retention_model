# customer_retention_model

### Problem
PADT is an engineering company based in Phoenix Arizona that specializes in numerical simulation, product development, and 3D Printing.  They have been in business for 25 years and have grown organically over that time.  Recently, they have found that their 3D Printing services business has been flat. They have never used customer data to look at retention and growth across their manufacturing offering.  PADT wants to know what they can do to retain and grow customers.  
The customer provided invoicing data for several years, basic customer information, a list of press releases, and classifications for customer industry and type of services provided. 


### Modeling Techniques
The models used logistic regression, gradient boost, and random forest classifiers. The gradient boost provided the most useful information, with 787 estimators and a maximum depth of 4.  This approach showed a log loss of 0.1999 and a ROC-AUC score of 0.9548. 


### Feature Engineering and Feature Importance
Deciding on which features to use began with looking at the quality of information given and then determining which features had an impact on total customer revenue and retention.  Time, geography, industry, and marketing were assessed in models to determine which led to useful information.  
The models showed that the most important features in predicting if a customer will return were the timing and topics of press releases, the industry a customer belonged to, and if a customer’s average order size was large. 


### Results & Conclusions
The modeling does a good job of predicting which customers are likely to not come back. The client should focus their sales efforts on getting those customers to return because other customers return without much effort.  That loyalty appears to be driven by the industry the customer comes from and how close the customer is to the client’s offices. 
Other indicators should be investigated further to understand the causes behind customer retention.  The unit price of the services being purchased has an impact on customer return, but the reason why is not clear.  Also, it would be beneficial to understand why customer who do business in the month of August are the most loyal. 
Reviewing the impact of press releases shows that the client should do more marketing that reminds customers of their services. The data indicates that a monthly newsletter would be beneficial. It also shows that users of the SLS 3D Printing process are the most loyal. The client believers that is because the SLS process is unique and hard to find.  Looking at adding other processes that are unique should lead to greater customer retention overall.
