# CME-Data-Engineer

## Description

Commodity futures and option contracts of many kinds are traded on NYMEX, owned by CME Group.  Each evening of each trading day, sometime between about 6:00 pm and 8:00 pm U.S. Central Time, a SPAN (Standard Portfolio Analysis of Risk) file is posted to cmegroup.com/ftp/span/data/cme containing information about the day’s trading. For a given day, the name of this file is cme.YYYYMMDD.c.pa2.zip, where YYYYMMDDD is the 8-digit year, month, and day of the file. Files for months prior to the current month are moved into a subdirectory of cmegroup.com/ftp/span/data/cme.

I have provided the SPAN file for Friday, July 9, 2021: cme.20210709.c.pa2.zip.  Download, unzip, then display this SPAN file. You will see that it is an enormous text file with its own unique format, unfortunately not something simple and convenient like CSV or XML or JSON.

The settlement prices (in U.S. dollars) contained in the SPAN file are used to mark to market each trader’s account, so that gains/losses can be credited/debited each day to reduce the risk of counterparty default (a trader who has to cover modest losses each day is less likely to default than a trader who has to cover huge losses at the end of a year, for example). This project is to extract these settlement prices, as well as contract expiration dates (last trading dates), for one of the most heavily traded global energy contracts: West Texas Intermediate (WTI) Crude Oil.

To learn about WTI Crude Oil futures contract details, see: http://www.cmegroup.com/trading/energy/crude-oil/light-sweet-crude_contract_specifications.html

![image](https://github.com/user-attachments/assets/7955b0c1-259f-40ed-9909-206b90cd5e56)

Notice that the CME Globex Product Code is CL; you will need this information for scanning the SPAN file. You can click QUOTES, SETTLEMENTS, VOLUME, etc., to see other characteristics of Crude Oil options and futures trading.

If you click the OPTIONS button, just to the right of the FUTURES button near the upper right, you will see information about options contracts based on the underlying futures contracts. There are about two dozen different types of option contracts for WTI Crude Oil futures; we are interested in the American Options (which seems to be the Type shown by default). When you look at the contract specifications, you will discover that its Product Code is LO.

Here are detailed examples of the structure of the Type B and Type 81 records for a different energy product, Natural Gas, for an earlier year.

B NYMNG        FUT201810            000000000900000001100030000330000000021643800000
001000020180926NG          00000000         0010000000000000 00 00 010000000000P 00 

According to the Type B Expanded documentation at https://www.cmegroup.com/confluence/display/pubspan/Type+B+-+Expanded

the Record ID (record type) is "B ",
the Exchange Acronym  is "NYM" 
the Commodity Code is "NG        " (for Natural Gas)		# futures code
the Product Type Code is "FUT" (futures contract)		# contract type
the contract month is "201810" (October, 2018)			# contract month
and the Expiration (Settlement) Date is "20180926"		# fut exp date  

You need to extract and reformat the Commodity Code, Product Type Code, Contract Month, and Expiration Date for Crude Oil (CL) records for the top half of the first table.  In your output table, these will be the Futures Code, Contract Type (display "Fut" rather than "FUT"), Contract Month, and Futures Exp Date, respectively

B NYMON        OOF201810   201810   002093720900000001100030000330000000021369900
000001000020180925NG        M 00000000N0280500+0010000000000000 00 00 010000000000P 00 

The Commodity Code is "ON        " ("LO        " for WTI crude)	# options code
the Product Type Code is "OOF" (option on futures)		# contract type
the contract month is "201810"					# contract month
the expiration date is "20180925"				# options exp date
The Underlying Commodity Code for this option is "NG        "  

This provides what you need to extract and reformat for the bottom half of the first table.  These correspond to the Options Code, Contract Type ("Call" or “Put”), Contract Month, and Options Exp Date.  The Futures Code for ON options is NG; the Futures Code for LO options is CL; you can know this from looking at the CME contract specification. 

B NYMNG        FUT201810            000000000900000001100030000330000000021643800000
001000020180926NG          00000000         0010000000000000 00 00 010000000000P 00 

According to the Type B Expanded documentation at https://www.cmegroup.com/confluence/display/pubspan/Type+B+-+Expanded

the Record ID (record type) is "B ",
the Exchange Acronym  is "NYM" 
the Commodity Code is "NG        " (for Natural Gas)		# futures code
the Product Type Code is "FUT" (futures contract)		# contract type
the contract month is "201810" (October, 2018)			# contract month
and the Expiration (Settlement) Date is "20180926"		# fut exp date  

You need to extract and reformat the Commodity Code, Product Type Code, Contract Month, and Expiration Date for Crude Oil (CL) records for the top half of the first table.  In your output table, these will be the Futures Code, Contract Type (display "Fut" rather than "FUT"), Contract Month, and Futures Exp Date, respectively

B NYMON        OOF201810   201810   002093720900000001100030000330000000021369900
000001000020180925NG        M 00000000N0280500+0010000000000000 00 00 010000000000P 00 

The Commodity Code is "ON        " ("LO        " for WTI crude)	# options code
the Product Type Code is "OOF" (option on futures)		# contract type
the contract month is "201810"					# contract month
the expiration date is "20180925"				# options exp date
The Underlying Commodity Code for this option is "NG        "  

This provides what you need to extract and reformat for the bottom half of the first table.  These correspond to the Options Code, Contract Type ("Call" or “Put”), Contract Month, and Options Exp Date.  The Futures Code for ON options is NG; the Futures Code for LO options is CL; you can know this from looking at the CME contract specification. 

For the second table, you will need to extract and reformat data from the Type 81 records.  Here are examples for Natural Gas.

For the first part of the second table:

81NYMNG        NG        FUT 201810            000000000000+00000+00367-00367-00367+00367+00733-00733-00733+00000000280500N 

The futures code is "NG        "				# commodity/product code
the contract month is "201810"				# fut contract month
the contract type is "FUT" 
and the settlement price is "00000000280500", which for natural gas you need to divide by 100000.0 to get 2.805 (natural gas prices are displayed to tenths of cents, unlike crude oil futures prices which are displayed to cents).  For WTI crude, you will need to figure out the correct divisor, by comparing the contents of the settlement price field with actual current WTI crude futures contract prices

For the second part of the second table:  

81NYMON        NG        OOFC201810   201810   000275000087-00100+00314-00133-00123+00311

The first record is for a call option (Option Right Code "C"), which is an option to buy a futures contract; the second record is for a put option (Option Right Code "P"), which is an option to sell a futures contract.  

The Underlying Commodity (Product) Code (futures code) is "NG        "
The Product Type Code is "OOF" (option on futures)
The Option Strike Price is "0002750" which you need to divide by 1000.0 to get 2.750,
 and the settlement price is "00000000000820" for the Call and 
"00000000000420" for the Put. 

Dividing by 10000.0, you get 0.082 as the price of a Call option, and 0.042 as the price of a Put option.  For WTI crude, you will only need to figure out one divisor, not two.

## Usage

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request with improvements or bug fixes.
## Credits
Author: Nora Ngo
