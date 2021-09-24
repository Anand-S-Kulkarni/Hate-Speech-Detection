# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 19:42:31 2020

@author: Madhuri
"""

from hatesonar import Sonar

class Custom:
    sonar = Sonar()
    def predict_classes(self, tweet):
        label = self.sonar.ping(tweet)
        if (label['top_class'] != 'neither'):
            return 1
        else:
            return 0
