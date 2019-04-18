# customer_retention_model

Problem
PADT is an engineering company based in Phoenix Arizona that specializes in numerical simulation, product development, and 3D Printing.  They have been in business for 25 years and have grown organically over that time.  Recently, they have found that their 3D Printing services business has been flat. They have never used customer data to look at retention and growth across their manufacturing offering.  PADT wants to know what they can do to retain and grow customers.  
The customer provided invoicing data for several years, basic customer information, a list of press releases, and classifications for customer industry and type of services provided. 


Modeling Techniques
The models used logistic regression, gradient boost, and random forest classifiers. The gradient boost provided the most useful information, with 787 estimators and a maximum depth of 4.  This approach showed a log loss of 0.1999 and a ROC-AUC score of 0.9548. 
