## Introduction

Malicious URL, a.k.a. malicious website, is a common and serious threat to cybersecurity. Malicious URLs host unsolicited content (spam, phishing, drive-by downloads, etc.) and lure unsuspecting users to become victims of scams (monetary loss, theft of private information, and malware installation), and cause losses of billions of dollars every year. It is imperative to detect and act on such threats in a timely manner. Traditionally, this detection is done mostly through the usage of blacklists. However, blacklists cannot be exhaustive, and lack the ability to detect newly generated malicious URLs. To improve the generality of malicious URL detectors, machine learning techniques have been explored with increasing attention in recent years. So, we aim in this Project to take advantage of Classification
techniques to predict whether a specific URL malicious od benign.

## Design And Data Description

Our Data Sources consist of tow Parts, First one is group of URLs that has been checked via whois command to verify
whether it isbenignorPhishingURL.
while second part is features of these URLs which have been fetched
via whois command too. the features were: whois_regDate, whois_expDate, whois_updatedDate, dot_count, url_len,
digit_count, special_count, hyphen_count, double_slash, single_slash, at_the_rate, protocol, and protocol_count.
Then we merged these Two Datasets to have data_df Dataframe.

## Tools:
• Pandas and Numpy (Exploring the data)

• Matplotlib and Seaborn (Visualizing the data)

• Sci-kit Learn (linear Regression model and other models)

• Xgboost

• Whois and tldextract

• FLASK API

