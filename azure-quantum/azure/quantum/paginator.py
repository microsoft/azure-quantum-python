##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
"""
Module providing the Paginator class, used to fetch paged items from
an Azure Quantum Workspace.
"""

from typing import Optional

class Paginator:
    """Class representing a pagination iterator"""

    def __init__(
        self,
        fetch_data_function,
        *,
        data_filter: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = 100,
        skip: Optional[int] = 0,
        **kwargs):
        """
        Initialize the Paginator.

        Args:
            fetch_data_function (callable): A function to fetch data. 
                                            It must accept `page_number` and `page_size` as arguments.
            page_size (int): Number of items per page. Default is 10.
            **kwargs: Additional arguments to pass to the fetch_data_function.
        """
        self.fetch_data_function = fetch_data_function
        self.filter = data_filter
        self.orderby = orderby
        self.top = top
        self.skip = skip
        self._kwargs = kwargs
        self._current_page_data = []
        self.has_next = True

    def fetch_data(self):
        """
        Fetch the current page of data.
        
        Returns:
            list: Data of the current page.
        """
        if not self._current_page_data:
            response = self.fetch_data_function(self._kwargs, filter=self.filter, orderby=self.orderby, top = self.top, skip = self.skip)
            self._current_page_data = response.data
            self.has_next = True if response.next_link is not None else False
            self.skip = self.skip + self.top
        return self._current_page_data
