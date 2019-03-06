"""
This file containg functions and classes related to data tranformation.
"""

import pandas as pd
from collections import namedtuple
from functools import partial


# Decorator allowing to specify a return class through the 
# optional kwarg 'return_class'.
def return_class(func):
    def func_wrapper(*args, **kwargs):
        return_class = Table
        if 'return_class' in kwargs.keys():
            return_class = kwargs.pop('return_class')
            assert return_class in Table.__subclasses__()
        return return_class(func(*args, **kwargs))
    return func_wrapper

class Table:
    """
    The Table class internally uses the pandas library to transform
    datasets. Usage in done through it's API and doesn't
    require any knowledge about pandas.
    input: pandas dataframe
    """
    def __init__(self, df):
        self._df = df
        self._main_column = self.column_names()[0]
        self._mockup_object = self._make_simple_object
        self._filter_df = False

    # Allow creation through a path and reader
    @staticmethod
    def make_table_from_path(path, reader):
        df = reader(path)
        return Table(df)

    # Return a Table or subclass where values of the specified column
    # are empty.
    @return_class
    def without(self, column):
        empty_entries = self._df[self._df[column].isnull()]
        return empty_entries

    # Return a Table or subclass where values of the specified column
    # are empty.
    @return_class
    def duplicate(self, column):
        duplicates_df = self._df[self._df[column].duplicated(keep=False)]
        return duplicates_df

    # Remove the df entries of another Table from this Table's
    # df, based on their index.
    @return_class
    def remove(self, *args):
        df = self._df
        for table in args:
            df = df.drop(table.get_df().index, errors='ignore')
        return df

    # Return the column names of the current df
    def column_names(self):
        return self._df.columns.values.tolist()

    # Return the df
    def get_df(self):
        return self._df

    # Merge two tables
    @return_class
    def merge(self, table, on, how="outer"):
        merged_dfs = pd.merge(self._df, table.get_df(), on=on, how=how)
        return merged_dfs

    # Filter out rows with any empty column value.
    def filter_nans(self):
        filterd_df = self._df[~self._df.isnull().any(axis=1)]
        return filterd_df

    def sort_by(self, columns, ascending=True):
        self._df = self._df.sort_values(by=columns, ascending=ascending)
 
    @return_class
    def most_frequent(self, groupby, count, top=10):
        grouped = self._df[[groupby, count]].groupby([groupby], as_index=False)
        counted = grouped.count()
        most_frequent = counted.nlargest(top, count)
        return most_frequent

    # Iterate over the df grouped by the main column and return 
    # each entry as a namedtuple.
    def __iter__(self):
        df = self._df
        if self._filter_df:
            df = self.filter_nans()

        for value in df[self._main_column].unique():
            yield self[value]
            # order = self._mockup_object(value=value)
            # yield order

    # Return a single df entry grouped by the main column a namedtuple.
    def __getitem__(self, value):
        order = self._mockup_object(value=value)
        return order

    def __eq__(self, other):
        return self.get_df().equals(other.get_df())

    # Return a namedtuple of a single df entry grouped by the main column 
    # as. Each column value can be accessed through the column name in the
    # namedtuple.
    def _make_simple_object(self, value, flatten=[]):
        name = self.__class__.__name__
        entry = self._df[self._df[self._main_column] == value]
        column_names = self.column_names()
        column_value_dict = {}

        for name in column_names:            
            if name in flatten:
                values = entry[name].values                
                if len(set(values)) == 1:

                    column_value_dict[name] = values[0]
                    continue
                print("ERROR: found multiple values, can't flatten {}".format(values))
                continue
            column_value_dict[name] = entry[name].tolist()

        NamedTuple = namedtuple(name, column_names)
        object_representation = NamedTuple(**column_value_dict)
        return object_representation

class Barcodes(Table):
    """ 
    A table specified for barcodes, groupby barcode for returned mockup objects.
    """
    def __init__(self, df):
        super(Barcodes, self).__init__(df)
        self._mockup_object = partial(self._make_simple_object,
                                      flatten=['barcode'])
        self._main_column = "barcode"

class Orders(Table):
    """ 
    A table specified for orders, groupby order_id and customer_id for returned 
    mockup objects. The inner datarepresentation, a pandas dataframe, filters 
    out rows with empty values.
    """
    def __init__(self, df):
        super(Orders, self).__init__(df)
        self._mockup_object = partial(self._make_simple_object,
                                      flatten=['order_id', 'customer_id'])
        self._main_column = "order_id"
        self._filter_df = True
