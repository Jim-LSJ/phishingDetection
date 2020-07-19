import os, sys
import bs4
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# a TOTAL_IP_LIST consist of all distinct ips
# In TOTAL_IP_LIST, {ip: {
#                       "first_ip": top 8 bits of ip
#                       "ASN": asn, "features in feature.csv": feature if ip is url_main_ip, else 0
#                       other feature of ip obtained by urlscan in the future will do
#                       }}

# Node Focus
# Node: domain IP (contain main ip and src ip)
# Edge: two types
#       1. main ip bidirected to src ip
#       2. IP with same ASN
# Node property: asn, top 8 or 16 bits IP, main ip can have features in feature.csv (src ip feature = 0)


