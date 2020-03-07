import re

class ACheck():
    def __init__(self):
        self.name = "TEST"
        self.critical = False
        self.warning = False
        self.unknown = False
    def is_critical(self, value):
        self.critical = True
    def is_warning(self, value):
        self.warining = True
    def is_unknown(self, value):
        self.unknown = True
    def check_metric(self, metric, warning=None, critical=None, ok=0):
        if metric > 0:
            self.is_critical(ok)
    def get_metric(self, column, regex):
        return True if isinstance(column, int) else False

metrics = {
    "erste":
    {
        2 : "3",
        "186" : "49171*"
    }
    }
m = { "key" : "value" }
a = ACheck()
a.check_metric(5)
print("CRITICAL: \t{}".format(a.critical))
print("WARNING: \t{}".format(a.warning))
for metric in metrics:
    print("METRIC: \t{}".format(metric))
    for column, regex in metrics[metric].items(): # py 2 iteritems
        print("{} {}".format(column, regex))
        m = a.get_metric(column, regex)
        print("I do some check magic and call get_metric \t {}".format(m))
