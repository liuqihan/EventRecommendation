
# coding: utf-8

# In[3]:


# 特征编码工具
#该事件涉及国家、城市、时间等信息的处理

#保存数据
import pickle

#特征编码
import datetime
import hashlib
# POSIX locale database and functionality
import locale
#国家的编码、名字、语言、货币等信息
import pycountry

import numpy as np
import scipy.io as sio
import scipy.sparse as ss

from collections import defaultdict
from sklearn.preprocessing import normalize

#类别型特征编码
#这里写成类的形式，因为编码字典要在不同的文件中使用
class FeatureEng:
  def __init__(self):
    
    # 载入 locales
    self.localeIdMap = defaultdict(int)
    for i, l in enumerate(locale.locale_alias.keys()):
      self.localeIdMap[l] = i + 1
    #print locale.locale_alias.keys()

    # 载入 countries
    self.countryIdMap = defaultdict(int)
    ctryIdx = defaultdict(int)
    for i, c in enumerate(pycountry.countries):
      self.countryIdMap[c.name.lower()] = i + 1
      if c.name.lower() == "usa":
        ctryIdx["US"] = i
      if c.name.lower() == "canada":
        ctryIdx["CA"] = i
    for cc in ctryIdx.keys():
      for s in pycountry.subdivisions.get(country_code=cc):
        self.countryIdMap[s.name.lower()] = ctryIdx[cc] + 1
        
    # 载入 gender id 字典
    ##缺失补0，性别未知
    self.genderIdMap = defaultdict(int, {'NaN': 0, "male":1, "female":2})

  def getLocaleId(self, locstr):
    return self.localeIdMap[locstr.lower()] #locstr.lower()返回将字符串locstr中所有大写字符转换为小写后生成的字符串

  def getGenderId(self, genderStr):
    return self.genderIdMap[genderStr]

  def getJoinedYearMonth(self, dateString):
    try:
        # 计算dateString距2010年1月过了多少个月
        dttm = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%S.%fZ")
        return (dttm.year-2010)*12 + dttm.month
    except:  #缺失补0
        return 0

  def getCountryId(self, location):
    if (isinstance(location, str)
        and len(location.strip()) > 0
        and location.rfind("  ") > -1):
        return self.countryIdMap[location[location.rindex("  ") + 2:].lower()]
    else:
        return 0

  def getBirthYearInt(self, birthYear):
    try:
      return 0 if birthYear == "None" else int(birthYear)
    except:
      return 0

  def getTimezoneInt(self, timezone):
    try:
      return int(timezone)
    except:
      return 0

  def getFeatureHash(self, value):
    if len(value.strip()) == 0: # strip()清除value两边的空白符，返回处理后的value
      return -1
    else:
      return int(hashlib.sha224(value.encode("utf-8")).hexdigest()[0:4], 16) # 哈希编码 把任意长度的数据转换为一个长度固定的数据串（通常用16进制的字符串表示）

  def getFloatValue(self, value):
    if len(value.strip()) == 0:
      return 0.0
    else:
      return float(value)

