# -*- coding: utf-8 -*-
import time

format_birth = "1985年05月24日10:30:00"

tup_birth = time.strptime(format_birth, "%Y年%m月%d日 %H:%M:%S");
birth_secds = time.mktime(tup_birth)
print birth_secds