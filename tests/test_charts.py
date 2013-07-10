  # -*- coding: utf-8 -*-
'''
Test Vincent.charts
-------------------

'''

import numpy as np
import pandas as pd
import nose.tools as nt
from vincent.charts import (data_type, Chart)


def test_data_type():
    """Test automatic data type importing"""

    puts = [[1], [1, 2], ((1, 2)), ((1, 2), (3, 4)), [(1, 2), (3, 4)],
            [[1, 2], [3, 4]], {1: 2}, {1: 2, 3: 4}]

    common = [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}]
    gets = [[{'x': 0, 'y': 1}], [{'x': 0, 'y': 1}, {'x': 1, 'y': 2}],
            [{'x': 0, 'y': 1}, {'x': 1, 'y': 2}], common, common,
            common, [{'x': 1, 'y': 2}], common]

    for ins, outs in zip(puts, gets):
        test = data_type(ins, False)
        nt.assert_list_equal(test.values, outs)

    #From Iters
    puts = [{'x': [1, 3], 'y': [2, 4]}, {'x': (1, 3), 'y': (2, 4)}]
    gets = [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}]

    for ins in puts:
        test = data_type(ins, True)
        nt.assert_list_equal(test.values, gets)

    #Pandas
    df = pd.DataFrame({'test': [1, 2, 3]})
    series = pd.Series([1, 2, 3], name='test')
    gets = [{'_index': 0, 'test': 1}, {'_index': 1, 'test': 2},
            {'_index': 2, 'test': 3}]
    test_df = data_type(df, False)
    test_series = data_type(series, False)
    nt.assert_list_equal(test_df.values, gets)
    nt.assert_list_equal(test_series.values, gets)

    #Bad type
    class BadType(object):
        """Bad data type"""
        pass

    test = BadType()
    nt.assert_raises(ValueError, data_type, test, False)
