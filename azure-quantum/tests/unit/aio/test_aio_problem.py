#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_solvers.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import pytest
from asyncmock import AsyncMock, patch, Mock
from azure.quantum.aio.optimization import Problem
from azure.quantum.optimization import Term
import azure.quantum.aio.optimization.problem
import azure.quantum.aio.job.base_job
from aio_common import expected_terms
import numpy
import os


@pytest.fixture
def mock_ws():
    mock_ws = AsyncMock()
    mock_ws.get_container_uri = AsyncMock(return_value = "mock_container_uri/foo/bar")
    return mock_ws


@pytest.fixture()
def problem():
    ## QUBO problem
    problem = Problem(name="test")
    problem.terms = [
        Term(c=3, indices=[1, 0]),
        Term(c=5, indices=[2, 0]),
    ]
    problem.uploaded_blob_uri = "mock_blob_uri"

    # Create equivalent NPZ file for translation
    problem.row = numpy.array([1, 2])
    problem.col = numpy.array([0, 0])
    problem.data = numpy.array([3, 5])
    return problem
    
@pytest.fixture
def default_qubo_problem(problem):
    # If arguments are passed to savez with no keywords
    # then default names are used (e.g. "arr_0", "arr_1", etc)
    # otherwise it uses those supplied by user (e.g. "row", "col", etc)
    default_qubo_filename = "default_qubo.npz"
    numpy.savez(default_qubo_filename, 
        problem.row,
        problem.col,
        problem.data
    )

    yield default_qubo_filename

    if os.path.isfile(default_qubo_filename):
        os.remove(default_qubo_filename)


@pytest.fixture
def with_keywords_qubo_problem(problem):
    fn = "with_keywords_qubo.npz"
    numpy.savez(fn,
        row=problem.row,
        col=problem.col,
        data=problem.data
    )
    yield fn
    if os.path.isfile(fn):
        os.remove(fn)


@pytest.fixture
def pubo_problem():
    ## PUBO problem
    pubo_problem = Problem(name="test")
    pubo_problem.terms = [
        Term(c=3, indices=[1, 0, 1]),
        Term(c=5, indices=[2, 0, 0]),
        Term(c=-1, indices=[1, 0, 0]),
        Term(c=4, indices=[0, 2, 1])
    ]

    # Create equivalent NPZ file for translation
    pubo_problem.i = numpy.array([1, 2, 1, 0])
    pubo_problem.j = numpy.array([0, 0, 0, 2])
    pubo_problem.k = numpy.array([1, 0, 0, 1])
    pubo_problem.c = numpy.array([3, 5, -1, 4])
    return pubo_problem

@pytest.fixture
def default_pubo_problem(pubo_problem):
    fn = "default_pubo.npz"
    numpy.savez(fn, 
        pubo_problem.i,
        pubo_problem.j,
        pubo_problem.k,
        pubo_problem.c
    )
    yield fn
    if os.path.isfile(fn):
        os.remove(fn)


@pytest.fixture
def with_keywords_pubo_problem(pubo_problem):
    fn = "with_keywords_pubo.npz"
    numpy.savez(fn,
        i=pubo_problem.i,
        j=pubo_problem.j,
        k=pubo_problem.k,
        c=pubo_problem.c
    )
    yield fn
    if os.path.isfile(fn):
        os.remove(fn)



@pytest.mark.asyncio    
async def test_upload(mock_ws, pubo_problem):
    with patch("azure.quantum.aio.optimization.problem.BlobClient") as mock_blob_client, \
        patch("azure.quantum.aio.optimization.problem.ContainerClient") as mock_container_client, \
        patch("azure.quantum.aio.job.base_job.upload_blob") as mock_upload:
        mock_blob_client.from_blob_url.return_value = Mock()
        mock_container_client.from_container_url.return_value = Mock()
        assert(pubo_problem.uploaded_blob_uri == None)
        actual_result = await pubo_problem.upload(mock_ws)
        mock_upload.get_blob_uri_with_sas_token = AsyncMock()
        azure.quantum.aio.job.base_job.upload_blob.assert_called_once()

@pytest.mark.asyncio
async def test_download(problem, mock_ws):
    with patch("azure.quantum.aio.optimization.problem.download_blob") as mock_download_blob,\
        patch("azure.quantum.aio.optimization.problem.BlobClient") as mock_blob_client,\
        patch("azure.quantum.aio.optimization.problem.ContainerClient") as mock_container_client:
        mock_download_blob.return_value=expected_terms()
        mock_blob_client.from_blob_url.return_value = Mock()
        mock_container_client.from_container_url.return_value = Mock()
        actual_result = await problem.download(mock_ws)
        assert actual_result.name == "test"
        azure.quantum.aio.optimization.problem.download_blob.assert_called_once()

def test_get_term(problem):
    terms = problem.get_terms(0)
    assert len(terms) == 2

def test_get_term_raise_exception():
    test_prob = Problem(name="random")
    with pytest.raises(Exception):
        test_prob.get_terms(id=0)

def test_create_npz_file_default(default_qubo_problem, default_pubo_problem):
    # When no keywords are supplied, columns have default names
    # e.g. "arr_0", "arr_1" etc
    
    # QUBO
    npz_file = numpy.load(default_qubo_problem)
    num_columns = 3

    assert len(npz_file.files) == num_columns
    for i in range(num_columns):
        assert npz_file.files[i] == "arr_%s" % i

    # PUBO
    npz_file = numpy.load(default_pubo_problem)
    num_columns = 4

    assert len(npz_file.files) == num_columns
    for i in range(num_columns):
        assert npz_file.files[i] == "arr_%s" % i

def test_create_npz_file_with_keywords(with_keywords_qubo_problem, with_keywords_pubo_problem):
    # When keywords are supplied, columns use these names

    # QUBO
    npz_file = numpy.load(with_keywords_qubo_problem)
    keywords = ["row", "col", "data"]

    assert len(npz_file.files) == len(keywords)
    for i in range(len(keywords)):
        assert npz_file.files[i] == keywords[i]

    # PUBO
    npz_file = numpy.load(with_keywords_pubo_problem)
    keywords = ["i", "j", "k", "c"]

    assert len(npz_file.files) == len(keywords)
    for i in range(len(keywords)):
        assert npz_file.files[i] == keywords[i] 

def test_valid_npz(problem, pubo_problem, default_qubo_problem, default_pubo_problem, with_keywords_qubo_problem, with_keywords_pubo_problem):
    default_qubo = numpy.load(default_qubo_problem)
    with_keywords_qubo = numpy.load(with_keywords_qubo_problem)

    default_pubo = numpy.load(default_pubo_problem)
    with_keywords_pubo = numpy.load(with_keywords_pubo_problem)

    ## Valid files
    assert problem.is_valid_npz(default_qubo.files)
    assert problem.is_valid_npz(
        default_qubo.files,
        ["arr_0", "arr_1"],
        "arr_2")

    assert problem.is_valid_npz(
        with_keywords_qubo.files,
        ["col", "row"],
        "data")

    assert pubo_problem.is_valid_npz(
        default_pubo.files,
        ["arr_0", "arr_1", "arr_2"],
        "arr_3")

    assert pubo_problem.is_valid_npz(
        with_keywords_pubo.files,
        ["i", "j", "k"],
        "c")

    ## Invalid files
    # Too many columns
    assert not problem.is_valid_npz(
        default_qubo.files,
        ["arr_0", "arr_1", "arr_2"],
        "arr_3")

    assert not pubo_problem.is_valid_npz(
        default_pubo.files,
        ["arr_0", "arr_1", "arr_2", "arr_3"],
        "arr_4")

    # Wrong column names
    assert not problem.is_valid_npz(
        with_keywords_qubo.files,
        ["i", "j"],
        "k")

    assert not pubo_problem.is_valid_npz(
        with_keywords_pubo.files,
        ["x", "y", "z"],
        "c")

    # No indices column names
    assert not problem.is_valid_npz(
        with_keywords_qubo.files,
        [],
        "data")

    # Wrong coefficient column name
    assert not problem.is_valid_npz(
        with_keywords_qubo.files,
        ["row", "col"], 
        "")

def test_invalid_file_path(problem):
    # Exceptions are raised for invalid file paths or files with incorrect naming
    with pytest.raises(Exception):
        problem.terms_from_npz("invalid_file_path.npz")

def test_invalid_terms_qubo(default_qubo_problem):
    with pytest.raises(Exception):
        problem.terms_from_npz (
            default_qubo_problem,
            ["arr_0", "arr_1", "arr_2"],
            "arr_3"
        )

def test_valid_files_produces_terms(problem, default_qubo_problem):
    # Terms are produced for valid files
    assert problem.terms_from_npz(default_qubo_problem) == problem.terms

def test_valid_keyword_files_produces_terms(problem, with_keywords_qubo_problem):
    assert problem.terms_from_npz(
            with_keywords_qubo_problem,
            ["row", "col"],
            "data"
        ) == problem.terms

def test_terms_from_npz_pubo(pubo_problem, default_pubo_problem):
    # Exceptions are raised for invalid file paths or files with incorrect naming
    with pytest.raises(Exception):
       pubo_problem.terms_from_npz("invalid_file_path.npz")
    with pytest.raises(Exception):
        pubo_problem.terms_from_npz (
            default_pubo_problem,
            ["arr_0", "arr_1", "arr_2", "arr_3"],
            "arr_4"
        )

def test_terms_are_produced_for_valid_files(pubo_problem, default_pubo_problem):
    # Terms are produced for valid files
    assert pubo_problem.terms_from_npz(
            default_pubo_problem,
            ["arr_0", "arr_1", "arr_2"],
            "arr_3"
        ) == pubo_problem.terms

def test_terms_are_produced_for_valid_files_with_keywords(pubo_problem, with_keywords_pubo_problem):
    assert pubo_problem.terms_from_npz(
            with_keywords_pubo_problem,
            ["i", "j", "k"],
            "c"
        ) == pubo_problem.terms
    