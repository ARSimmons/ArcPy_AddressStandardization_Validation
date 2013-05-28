###############################################
## Arielle Simmons                           ##
## Planner/GIS Specialist                    ##
## Pioneer Valley Planning Commission        ##
## Date created: November 29, 2010           ##
## Date modified:                            ##
###############################################
## This script searches for and replaces a key word based its
## dictionary conjugate.
## This is an in-string search and replace operation
## You MUST set the workspace (at the moment,
## this is intended to be the folder with a file gdb loaded in it)
## in order to begin the search.

## Note 4/22/13 Update ##
###############################################################################################
## In the case of directionals the user will be asked 'Y' or 'N' on replacing the identified ##
## direction. The reason for this is the USPS standards for abbriviating directionals        ##
## vary. Please make sure the user is knowlegable about these variances BEFORE running the   ##
## script!                                                                                   ##
##                                                                                           ##
## If the user selects 'Y' for replacing a directional, the replace keyword will show        ##
## up with '\b' before and after the word (ex: '\bEAST\b'). This '\b' is only shown in the   ##
## shell output...and will not be shown in the database output.                              ##        
##                                                                                           ##
## When search and replacing for direction prefixes (East, West, North, South)               ##
## If a direction is both the prefix, and the street name (ex: East North Street)            ##
## The algorithm asks the user if it should "Abbreviate Keyword X" twice for the same address##
## (i.e. once for "EAST" and once for "NORTH").                                              ##
##                                                                                           ##
##                                                                                           ##
## !!!IMPORTANT!!! Because the function is doing a 'multiple replace' if you say 'Y' to      ##
## replacing the 'NORTH' in 'EAST NORTH STREET' you also will be replacing 'EAST'            ##
## as well (without being asked again for the term 'EAST'). IT IS IMPORTANT THAT THE USER    ##
## KNOW THAT IN THE USPS GUIDELEINES : "WHEN TWO DIRECTIONAL WORDS APPEAR CONSECUTIVELY AS   ##
## ONE OR TWO WORDS...(any) COMBINATIONS OF NORTH-SOUTH or EAST-WEST (should) APPEAR AS      ##
## CONSECUTIVE WORDS"                                                                        ##
##                                                                                           ##
## THEREFORE in the case of 'EAST NORTH STREET' the user should ALWAYS say 'N' FOR replacing ##
## BOTH OF THE DIRECTIONAL(s).                                                               ##
##                                                                                           ##
## OVERALL, because of the two directional problem this part of the function                 ##
## could more efficient...                                                                   ##
## the repeat user input needs to be cut out. However, the main                              ##
## goal here was to be able to catch pre/post fix's...                                       ##
## That said, there is not time to fix it right now.                                         ##
###############################################################################################

# Import modules

import arcpy
import os
import sys

# Python module for regular expressions

import re

from arcpy import env

# define variable "myWorkspace" to the folder where
# the File geodatabase is. Within the databases fields
# there should be an Address field (in one of the feature classes or tables)
# called "SITE_ADDR" (which is a MassGIS standard field name)

myWorkspace = r"C:\Users\asimmons\Desktop\Code_Test\Regular_Expression_ArcGIS_AddressStandardization\Test_DB"

arcpy.env.workspace = myWorkspace

# Overwrite pre-existing workspace

arcpy.env.overwriteOutput = True


# Set the data dictionary
# The conjugate pairs were taken directly from the United States Postal Service

suf_dictionary={
    r'\bALLEE$':'ALY',
    r'\bALLEY$':'ALY',
    r'\bALLY$':'ALY',
    r'\bALY$':'ALY',
    r'\bANEX$':'ANX',
    r'\bANNEX$':'ANX',
    r'\bANNX$':'ANX',
    r'\bANX$':'ANX',
    r'\bARC$':'ARC',
    r'\bARCADE$':'ARC',
    r'\bAV$':'AVE',
    r'\bAVE$':'AVE',
    r'\bAVEN$':'AVE',
    r'\bAVENU$':'AVE',
    r'\bAVENUE$':'AVE',
    r'\bAVN$':'AVE',
    r'\bAVNUE$':'AVE',
    r'\bBAYOO$':'BYU',
    r'\bBAYOU$':'BYU',
    r'\bBCH$':'BCH',
    r'\bBEACH$':'BCH',
    r'\bBEND$':'BND',
    r'\bBND$':'BND',
    r'\bBLF$':'BLF',
    r'\bBLUF$':'BLF',
    r'\bBLUFF$':'BLF',
    r'\bBLUFFS$':'BLFS',
    r'\bBOT$':'BTM',
    r'\bBOTTM$':'BTM',
    r'\bBOTTOM$':'BTM',
    r'\bBTM$':'BTM',
    r'\bBLVD$':'BLVD',
    r'\bBOUL$':'BLVD',
    r'\bBOULEVARD$':'BLVD',
    r'\bBOULV$':'BLVD',
    r'\bBR$':'BR',
    r'\bBRANCH$':'BR',
    r'\bBRNCH$':'BR',
    r'\bBRDGE$':'BRG',
    r'\bBRG$':'BRG',
    r'\bBRIDGE$':'BRG',
    r'\bBRK$':'BRK',
    r'\bBROOK$':'BRK',
    r'\bBROOKS$':'BRKS',
    r'\bBURG$':'BG',
    r'\bBURGS$':'BGS',
    r'\bBYP$':'BYP',
    r'\bBYPA$':'BYP',
    r'\bBYPAS$':'BYP',
    r'\bBYPASS$':'BYP',
    r'\bBYPS$':'BYP',
    r'\bCAMP$':'CP',
    r'\bCMP$':'CP',
    r'\bCP$':'CP',
    r'\bCANYN$':'CYN',
    r'\bCANYON$':'CYN',
    r'\bCNYN$':'CYN',
    r'\bCYN$':'CYN',
    r'\bCAPE$':'CPE',
    r'\bCPE$':'CPE',
    r'\bCAUSEWAY$':'CSWY',
    r'\bCAUSWAY$':'CSWY',
    r'\bCSWY$':'CSWY',
    r'\bCEN$':'CTR',
    r'\bCENT$':'CTR',
    r'\bCENTER$':'CTR',
    r'\bCENTR$':'CTR',
    r'\bCENTRE$':'CTR',
    r'\bCNTER$':'CTR',
    r'\bCNTR$':'CTR',
    r'\bCTR$':'CTR',
    r'\bCENTERS$':'CTRS',
    r'\bCIR$':'CIR',
    r'\bCIRC$':'CIR',
    r'\bCIRCL$':'CIR',
    r'\bCIRCLE$':'CIR',
    r'\bCRCL$':'CIR',
    r'\bCRCLE$':'CIR',
    r'\bCIRCLES$':'CIRS',
    r'\bCLF$':'CLF',
    r'\bCLIFF$':'CLF',
    r'\bCLFS$':'CLFS',
    r'\bCLIFFS$':'CLFS',
    r'\bCLB$':'CLB',
    r'\bCLUB$':'CLB',
    r'\bCOMMON$':'CMN',
    r'\bCOR$':'COR',
    r'\bCORNER$':'COR',
    r'\bCORNERS$':'CORS',
    r'\bCORS$':'CORS',
    r'\bCOURSE$':'CRSE',
    r'\bCRSE$':'CRSE',
    r'\bCOURT$':'CT',
    r'\bCRT$':'CT',
    r'\bCT$':'CT',
    r'\bCOURTS$':'CTS',
    r'\bCTS$':'CTS',
    r'\bCOVE$':'CV',
    r'\bCV$':'CV',
    r'\bCOVES$':'CVS',
    r'\bCK$':'CRK',
    r'\bCR$':'CRK',
    r'\bCREEK$':'CRK',
    r'\bCRK$':'CRK',
    r'\bCRECENT$':'CRES',
    r'\bCRES$':'CRES',
    r'\bCRESCENT$':'CRES',
    r'\bCRESENT$':'CRES',
    r'\bCRSCNT$':'CRES',
    r'\bCRSENT$':'CRES',
    r'\bCRSNT$':'CRES',
    r'\bCREST$':'CRST',
    r'\bCROSSING$':'XING',
    r'\bCRSSING$':'XING',
    r'\bCRSSNG$':'XING',
    r'\bXING$':'XING',
    r'\bCROSSROAD$':'XRD',
    r'\bCURVE$':'CURV',
    r'\bDALE$':'DL',
    r'\bDL$':'DL',
    r'\bDAM$':'DM',
    r'\bDM$':'DM',
    r'\bDIV$':'DV',
    r'\bDIVIDE$':'DV',
    r'\bDV$':'DV',
    r'\bDVD$':'DV',
    r'\bDR$':'DR',
    r'\bDRIV$':'DR',
    r'\bDRIVE$':'DR',
    r'\bDRV$':'DR',
    r'\bDRIVES$':'DRS',
    r'\bEST$':'EST',
    r'\bESTATE$':'EST',
    r'\bESTATES$':'ESTS',
    r'\bESTS$':'ESTS',
    r'\bEXP$':'EXPY',
    r'\bEXPR$':'EXPY',
    r'\bEXPRESS$':'EXPY',
    r'\bEXPRESSWAY$':'EXPY',
    r'\bEXPW$':'EXPY',
    r'\bEXPY$':'EXPY',
    r'\bEXT$':'EXT',
    r'\bEXTENSION$':'EXT',
    r'\bEXTN$':'EXT',
    r'\bEXTNSN$':'EXT',
    r'\bEXTENSIONS$':'EXTS',
    r'\bEXTS$':'EXTS',
    r'\bFALL$':'FALL',
    r'\bFALLS$':'FLS',
    r'\bFLS$':'FLS',
    r'\bFERRY$':'FRY',
    r'\bFRRY$':'FRY',
    r'\bFRY$':'FRY',
    r'\bFIELD$':'FLD',
    r'\bFLD$':'FLD',
    r'\bFIELDS$':'FLDS',
    r'\bFLDS$':'FLDS',
    r'\bFLAT$':'FLT',
    r'\bFLT$':'FLT',
    r'\bFLATS$':'FLTS',
    r'\bFLTS$':'FLTS',
    r'\bFORD$':'FRD',
    r'\bFRD$':'FRD',
    r'\bFORDS$':'FRDS',
    r'\bFOREST$':'FRST',
    r'\bFORESTS$':'FRST',
    r'\bFRST$':'FRST',
    r'\bFORG$':'FRG',
    r'\bFORGE$':'FRG',
    r'\bFRG$':'FRG',
    r'\bFORGES$':'FRGS',
    r'\bFORK$':'FRK',
    r'\bFRK$':'FRK',
    r'\bFORKS$':'FRKS',
    r'\bFRKS$':'FRKS',
    r'\bFORT$':'FT',
    r'\bFRT$':'FT',
    r'\bFT$':'FT',
    r'\bFREEWAY$':'FWY',
    r'\bFREEWY$':'FWY',
    r'\bFRWAY$':'FWY',
    r'\bFRWY$':'FWY',
    r'\bFWY$':'FWY',
    r'\bGARDEN$':'GDN',
    r'\bGARDN$':'GDN',
    r'\bGDN$':'GDN',
    r'\bGRDEN$':'GDN',
    r'\bGRDN$':'GDN',
    r'\bGARDENS$':'GDNS',
    r'\bGDNS$':'GDNS',
    r'\bGRDNS$':'GDNS',
    r'\bGATEWAY$':'GTWY',
    r'\bGATEWY$':'GTWY',
    r'\bGATWAY$':'GTWY',
    r'\bGTWAY$':'GTWY',
    r'\bGTWY$':'GTWY',
    r'\bGLEN$':'GLN',
    r'\bGLN$':'GLN',
    r'\bGLENS$':'GLNS',
    r'\bGREEN$':'GRN',
    r'\bGRN$':'GRN',
    r'\bGREENS$':'GRNS',
    r'\bGROV$':'GRV',
    r'\bGROVE$':'GRV',
    r'\bGRV$':'GRV',
    r'\bGROVES$':'GRVS',
    r'\bHARB$':'HBR',
    r'\bHARBOR$':'HBR',
    r'\bHARBR$':'HBR',
    r'\bHBR$':'HBR',
    r'\bHRBOR$':'HBR',
    r'\bHARBORS$':'HBRS',
    r'\bHAVEN$':'HVN',
    r'\bHAVN$':'HVN',
    r'\bHVN$':'HVN',
    r'\bHEIGHT$':'HTS',
    r'\bHEIGHTS$':'HTS',
    r'\bHGTS$':'HTS',
    r'\bHT$':'HTS',
    r'\bHTS$':'HTS',
    r'\bHIGHWAY$':'HWY',
    r'\bHIGHWY$':'HWY',
    r'\bHIWAY$':'HWY',
    r'\bHIWY$':'HWY',
    r'\bHWAY$':'HWY',
    r'\bHWY$':'HWY',
    r'\bHILL$':'HL',
    r'\bHL$':'HL',
    r'\bHILLS$':'HLS',
    r'\bHLS$':'HLS',
    r'\bHLLW$':'HOLW',
    r'\bHOLLOW$':'HOLW',
    r'\bHOLLOWS$':'HOLW',
    r'\bHOLW$':'HOLW',
    r'\bHOLWS$':'HOLW',
    r'\bINLET$':'INLT',
    r'\bINLT$':'INLT',
    r'\bIS$':'IS',
    r'\bISLAND$':'IS',
    r'\bISLND$':'IS',
    r'\bISLANDS$':'ISS',
    r'\bISLNDS$':'ISS',
    r'\bISS$':'ISS',
    r'\bISLE$':'ISLE',
    r'\bISLES$':'ISLE',
    r'\bJCT$':'JCT',
    r'\bJCTION$':'JCT',
    r'\bJCTN$':'JCT',
    r'\bJUNCTION$':'JCT',
    r'\bJUNCTN$':'JCT',
    r'\bJUNCTON$':'JCT',
    r'\bJCTNS$':'JCTS',
    r'\bJCTS$':'JCTS',
    r'\bJUNCTIONS$':'JCTS',
    r'\bKEY$':'KY',
    r'\bKY$':'KY',
    r'\bKEYS$':'KYS',
    r'\bKYS$':'KYS',
    r'\bKNL$':'KNL',
    r'\bKNOL$':'KNL',
    r'\bKNOLL$':'KNL',
    r'\bKNLS$':'KNLS',
    r'\bKNOLLS$':'KNLS',
    r'\bLAKE$':'LK',
    r'\bLK$':'LK',
    r'\bLAKES$':'LKS',
    r'\bLKS$':'LKS',
    r'\bLAND$':'LAND',
    r'\bLANDING$':'LNDG',
    r'\bLNDG$':'LNDG',
    r'\bLNDNG$':'LNDG',
    r'\bLA$':'LN',
    r'\bLANE$':'LN',
    r'\bLANES$':'LN',
    r'\bLN$':'LN',
    r'\bLGT$':'LGT',
    r'\bLIGHT$':'LGT',
    r'\bLIGHTS$':'LGTS',
    r'\bLF$':'LF',
    r'\bLOAF$':'LF',
    r'\bLCK$':'LCK',
    r'\bLOCK$':'LCK',
    r'\bLCKS$':'LCKS',
    r'\bLOCKS$':'LCKS',
    r'\bLDG$':'LDG',
    r'\bLDGE$':'LDG',
    r'\bLODG$':'LDG',
    r'\bLODGE$':'LDG',
    r'\bLOOP$':'LOOP',
    r'\bLOOPS$':'LOOP',
    r'\bMALL$':'MALL',
    r'\bMANOR$':'MNR',
    r'\bMNR$':'MNR',
    r'\bMANORS$':'MNRS',
    r'\bMNRS$':'MNRS',
    r'\bMDW$':'MDW',
    r'\bMEADOW$':'MDW',
    r'\bMDWS$':'MDWS',
    r'\bMEADOWS$':'MDWS',
    r'\bMEDOWS$':'MDWS',
    r'\bMEWS$':'MEWS',
    r'\bMILL$':'ML',
    r'\bML$':'ML',
    r'\bMILLS$':'MLS',
    r'\bMLS$':'MLS',
    r'\bMISSION$':'MSN',
    r'\bMISSN$':'MSN',
    r'\bMSN$':'MSN',
    r'\bMSSN$':'MSN',
    r'\bMOTORWAY$':'MTWY',
    r'\bMNT$':'MT',
    r'\bMOUNT$':'MT',
    r'\bMT$':'MT',
    r'\bMNTAIN$':'MTN',
    r'\bMNTN$':'MTN',
    r'\bMOUNTAIN$':'MTN',
    r'\bMOUNTIN$':'MTN',
    r'\bMTIN$':'MTN',
    r'\bMTN$':'MTN',
    r'\bMNTNS$':'MTNS',
    r'\bMOUNTAINS$':'MTNS',
    r'\bNCK$':'NCK',
    r'\bNECK$':'NCK',
    r'\bORCH$':'ORCH',
    r'\bORCHARD$':'ORCH',
    r'\bORCHRD$':'ORCH',
    r'\bOVAL$':'OVAL',
    r'\bOVL$':'OVAL',
    r'\bOVERPASS$':'OPAS',
    r'\bPARK$':'PARK',
    r'\bPK$':'PARK',
    r'\bPRK$':'PARK',
    r'\bPARKS$':'PARK',
    r'\bPARKWAY$':'PKWY',
    r'\bPARKWY$':'PKWY',
    r'\bPKWAY$':'PKWY',
    r'\bPKWY$':'PKWY',
    r'\bPKY$':'PKWY',
    r'\bPARKWAYS$':'PKWY',
    r'\bPKWYS$':'PKWY',
    r'\bPASS$':'PASS',
    r'\bPASSAGE$':'PSGE',
    r'\bPATH$':'PATH',
    r'\bPATHS$':'PATH',
    r'\bPIKE$':'PIKE',
    r'\bPIKES$':'PIKE',
    r'\bPINE$':'PNE',
    r'\bPINES$':'PNES',
    r'\bPNES$':'PNES',
    r'\bPL$':'PL',
    r'\bPLACE$':'PL',
    r'\bPLAIN$':'PLN',
    r'\bPLN$':'PLN',
    r'\bPLAINES$':'PLNS',
    r'\bPLAINS$':'PLNS',
    r'\bPLNS$':'PLNS',
    r'\bPLAZA$':'PLZ',
    r'\bPLZ$':'PLZ',
    r'\bPLZA$':'PLZ',
    r'\bPOINT$':'PT',
    r'\bPT$':'PT',
    r'\bPOINTS$':'PTS',
    r'\bPTS$':'PTS',
    r'\bPORT$':'PRT',
    r'\bPRT$':'PRT',
    r'\bPORTS$':'PRTS',
    r'\bPRTS$':'PRTS',
    r'\bPR$':'PR',
    r'\bPRAIRIE$':'PR',
    r'\bPRARIE$':'PR',
    r'\bPRR$':'PR',
    r'\bRAD$':'RADL',
    r'\bRADIAL$':'RADL',
    r'\bRADIEL$':'RADL',
    r'\bRADL$':'RADL',
    r'\bRAMP$':'RAMP',
    r'\bRANCH$':'RNCH',
    r'\bRANCHES$':'RNCH',
    r'\bRNCH$':'RNCH',
    r'\bRNCHS$':'RNCH',
    r'\bRAPID$':'RPD',
    r'\bRPD$':'RPD',
    r'\bRAPIDS$':'RPDS',
    r'\bRPDS$':'RPDS',
    r'\bREST$':'RST',
    r'\bRST$':'RST',
    r'\bRDG$':'RDG',
    r'\bRDGE$':'RDG',
    r'\bRIDGE$':'RDG',
    r'\bRDGS$':'RDGS',
    r'\bRIDGES$':'RDGS',
    r'\bRIV$':'RIV',
    r'\bRIVER$':'RIV',
    r'\bRIVR$':'RIV',
    r'\bRVR$':'RIV',
    r'\bRD$':'RD',
    r'\bROAD$':'RD',
    r'\bRDS$':'RDS',
    r'\bROADS$':'RDS',
    r'\bROUTE$':'RTE',
    r'\bROW$':'ROW',
    r'\bRUE$':'RUE',
    r'\bRUN$':'RUN',
    r'\bSHL$':'SHL',
    r'\bSHOAL$':'SHL',
    r'\bSHLS$':'SHLS',
    r'\bSHOALS$':'SHLS',
    r'\bSHOAR$':'SHR',
    r'\bSHORE$':'SHR',
    r'\bSHR$':'SHR',
    r'\bSHOARS$':'SHRS',
    r'\bSHORES$':'SHRS',
    r'\bSHRS$':'SHRS',
    r'\bSKYWAY$':'SKWY',
    r'\bSPG$':'SPG',
    r'\bSPNG$':'SPG',
    r'\bSPRING$':'SPG',
    r'\bSPRNG$':'SPG',
    r'\bSPGS$':'SPGS',
    r'\bSPNGS$':'SPGS',
    r'\bSPRINGS$':'SPGS',
    r'\bSPRNGS$':'SPGS',
    r'\bSPUR$':'SPUR',
    r'\bSPURS$':'SPUR',
    r'\bSQ$':'SQ',
    r'\bSQR$':'SQ',
    r'\bSQRE$':'SQ',
    r'\bSQU$':'SQ',
    r'\bSQUARE$':'SQ',
    r'\bSQRS$':'SQS',
    r'\bSQUARES$':'SQS',
    r'\bSTA$':'STA',
    r'\bSTATION$':'STA',
    r'\bSTATN$':'STA',
    r'\bSTN$':'STA',
    r'\bSTRA$':'STRA',
    r'\bSTRAV$':'STRA',
    r'\bSTRAVE$':'STRA',
    r'\bSTRAVEN$':'STRA',
    r'\bSTRAVENUE$':'STRA',
    r'\bSTRAVN$':'STRA',
    r'\bSTRVN$':'STRA',
    r'\bSTRVNUE$':'STRA',
    r'\bSTREAM$':'STRM',
    r'\bSTREME$':'STRM',
    r'\bSTRM$':'STRM',
    r'\bST$':'ST',
    r'\bSTR$':'ST',
    r'\bSTREET$':'ST',
    r'\bSTRT$':'ST',
    r'\bSTREETS$':'STS',
    r'\bSMT$':'SMT',
    r'\bSUMIT$':'SMT',
    r'\bSUMITT$':'SMT',
    r'\bSUMMIT$':'SMT',
    r'\bTER$':'TER',
    r'\bTERR$':'TER',
    r'\bTERRACE$':'TER',
    r'\bTHROUGHWAY$':'TRWY',
    r'\bTRACE$':'TRCE',
    r'\bTRACES$':'TRCE',
    r'\bTRCE$':'TRCE',
    r'\bTRACK$':'TRAK',
    r'\bTRACKS$':'TRAK',
    r'\bTRAK$':'TRAK',
    r'\bTRK$':'TRAK',
    r'\bTRKS$':'TRAK',
    r'\bTRAFFICWAY$':'TRFY',
    r'\bTRFY$':'TRFY',
    r'\bTR$':'TRL',
    r'\bTRAIL$':'TRL',
    r'\bTRAILS$':'TRL',
    r'\bTRL$':'TRL',
    r'\bTRLS$':'TRL',
    r'\bTUNEL$':'TUNL',
    r'\bTUNL$':'TUNL',
    r'\bTUNLS$':'TUNL',
    r'\bTUNNEL$':'TUNL',
    r'\bTUNNELS$':'TUNL',
    r'\bTUNNL$':'TUNL',
    r'\bTPK$':'TPKE',
    r'\bTPKE$':'TPKE',
    r'\bTRNPK$':'TPKE',
    r'\bTRPK$':'TPKE',
    r'\bTURNPIKE$':'TPKE',
    r'\bTURNPK$':'TPKE',
    r'\bUNDERPASS$':'UPAS',
    r'\bUN$':'UN',
    r'\bUNION$':'UN',
    r'\bUNIONS$':'UNS',
    r'\bVALLEY$':'VLY',
    r'\bVALLY$':'VLY',
    r'\bVLLY$':'VLY',
    r'\bVLY$':'VLY',
    r'\bVALLEYS$':'VLYS',
    r'\bVLYS$':'VLYS',
    r'\bVDCT$':'VIA',
    r'\bVIA$':'VIA',
    r'\bVIADCT$':'VIA',
    r'\bVIADUCT$':'VIA',
    r'\bVIEW$':'VW',
    r'\bVW$':'VW',
    r'\bVIEWS$':'VWS',
    r'\bVWS$':'VWS',
    r'\bVILL$':'VLG',
    r'\bVILLAG$':'VLG',
    r'\bVILLAGE$':'VLG',
    r'\bVILLG$':'VLG',
    r'\bVILLIAGE$':'VLG',
    r'\bVLG$':'VLG',
    r'\bVILLAGES$':'VLGS',
    r'\bVLGS$':'VLGS',
    r'\bVILLE$':'VL',
    r'\bVL$':'VL',
    r'\bVIS$':'VIS',
    r'\bVIST$':'VIS',
    r'\bVISTA$':'VIS',
    r'\bVST$':'VIS',
    r'\bVSTA$':'VIS',
    r'\bWALK$':'WALK',
    r'\bWALKS$':'WALK',
    r'\bWALL$':'WALL',
    r'\bWAY$':'WAY',
    r'\bWY$':'WAY',
    r'\bWAYS$':'WAYS',
    r'\bWELL$':'WL',
    r'\bWELLS$':'WLS',
    r'\bWLS$':'WLS',
    r'\bROAD\b':'RD',
    r'\.':'',
    r'\bFIRST\b':'1ST',
    r'\bSECOND\b':'2ND',
    r'\bTHIRD\b':'3RD',
    r'\bFOURTH\b':'4TH',
    r'\bFIFTH\b':'5TH',
    r'\bSIXTH\b':'6TH',
    r'\bSEVENTH\b':'7TH',
    r'\bEIGTHTH\b':'8TH',
    r'\bNINTH\b':'9TH',
    r'\bTENTH\b':'10TH',
    r'\bELEVENTH\b':'11TH',
    r'\bTWELFTH\b':'12TH',
    r'\bTHIRTEENTH\b':'13TH',
    r'\bFOURTEENTH\b':'14TH',
    r'\bFIFTEENTH\b':'15TH',
    r'\bSIXTEENTH\b':'16TH',
    r'\bSEVENTEENTH\b':'17TH',
    r'\bEIGHTEENTH\b':'18TH',
    r'\bNINETEENTH\b':'19TH',
    }

dir_dictionary={
    r'\bEAST\b':'E',
    r'\bWEST\b':'W',
    r'\bNORTH\b':'N',
    r'\bSOUTH\b':'S',
    }

dir_pattern=[r'\bEAST\b',r'\bWEST\b',r'\bNORTH\b',r'\bSOUTH\b']

#Create a function to find and replace according to the dictionary
#This function uses "regular expressions" from the 're' module for search and replace

def multiple_replace(text,dictionary):
    for i, j in dictionary.iteritems():
        text=re.sub(i,j,text)
    return text

# Create a function to:
# 1) Run ListFields within ALL the Feature classes and Tables within the directory.
# 2) Search for a field called "SITE_ADDR".
# 3) Add an update field in that feature class called "SITE_ADDR_2"
# (if it does not already exist)
# 4) and then populate it with what is in "SITE_ADDR".

# After Steps 1-4 complete
# the 'find_address_field' function loops through the rows within
# the "SITE_ADDR_2" field and uses the 'multiple_replace'
# function to modify the addresses.
# NOTE: A lot of examples use a WHILE loop to do this...
# for a test in efficiency, and reducing the re-placing of the
# Search/Update cursor...I am using a FOR loop....

def find_address_field(object):
    # List the fields in the feature class and/or table
    # an 'object' can be a field within either of these
    fieldList = arcpy.ListFields(object)
    for field in fieldList:
        if field.name == "SITE_ADDR":
            UpdateField = "SITE_ADDR_2"
            if not UpdateField in fieldList:
                arcpy.AddField_management(object, UpdateField, "text", "150")
                arcpy.CalculateField_management(object, "SITE_ADDR_2", "!SITE_ADDR!", "PYTHON")
            # Open a update cursor to go through the address field 
            rows = arcpy.UpdateCursor(object)

            # Go through all the rows to find and replace key words according to the dictionary
            for row in rows:

                # The Row will be checked for case structure, and capitalized if not in the correct
                # case
                Adrs = row.SITE_ADDR_2.upper()

                # standardize the addresses via the post office rules
                # using the function multiple_replace
                Adrs = multiple_replace(Adrs, suf_dictionary)

                print Adrs
                
                # Direction prefixes are a special case because they can be proper street names
                # as well as prefixes for street names (East, West, North, South)
                # This section of code prompts the user for a decision
                # about whether or not to replace a direction in the street
                # name with its abbreviation

                # In the shell, it is going to add '\b' to the front and
                # back of the output...but that doesn't mean it is changing the
                # output in the database to this...it is only showing the
                # list object in the shell...

                for direction in dir_pattern:
                    if re.search(direction, Adrs):
                        print Adrs
                        print 'Replace Keyword: ',direction
                        choice=raw_input('Y/N')
                        if (choice == 'Y') or (choice == 'y'):
                            Adrs = multiple_replace(Adrs, dir_dictionary)
                            print 'You have chosen to REPLACE the keyword', direction
                        else: print 'You have chosen NOT to replace this keyword'

                # Change the variable 'Adrs' back to the database row information
                row.SITE_ADDR_2 = Adrs
                
                # Physically update the address in the table
                rows.updateRow(row)

    # Delete cursor and row objects to remove locks on the data
    del row, rows

# Set the geoprocessor to the current workspace/folder (i.e. myWorkspace)
# List all Geodatabases in the current workspace/folder


workspace_gdb = arcpy.ListWorkspaces("*", "FileGDB")

for gdb in workspace_gdb:
    print gdb

    # redefine the workspace as the geodatabase

    arcpy.env.workspace = gdb

    # Get into Feature classes and tables within a Feature Dataset 
    datasetList = arcpy.ListDatasets()
    for dataset in datasetList:
        print dataset

        # redefine the workspace as the feature dataset

        arcpy.env.workspace = dataset

        # List all the feature classes and tables
        # that are within the FileGDB feature dataset
        
        fcs = arcpy.ListFeatureClasses()
        for fc in fcs:
            print fc
            find_address_field(fc)
            print find_address_field(fc)


        tableList = arcpy.ListTables()
        for table in tableList:
            print table
            find_address_field(table)
            print find_address_field(table)
    # redefine the workspace as the geodatabase (not the dataset)

    arcpy.env.workspace = gdb

    # List the feature classes in the current FileGDB (That are NOT within a dataset)
        
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
        print fc
        find_address_field(fc)
        print find_address_field(fc)
    
    # List the tables in the current FileGDB (That are NOT within a dataset)

    tableList = arcpy.ListTables()
    for table in tableList:
        print table
        find_address_field(table)
        print find_address_field(table)
 

                
