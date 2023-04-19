##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from urllib.request import urlopen

def df_chemistry() -> bytes:
    """
    Returns bitcode of a QIR program for the double-factorized chemistry
    quantum algorithm.
    """
    return urlopen("https://aka.ms/RE/df_chemistry").read()
