import pytest
from main import *


def test_sync():
    left = Map(
        name="left",
        source_destination_maps=[
            SourceDestinationMap(0, 0, 100, default=True),
        ],
    )
    right = Map(
        name="right",
        source_destination_maps=[
            SourceDestinationMap(0, 0, 50, default=True),
            SourceDestinationMap(50, 0, 50, default=True),
        ],
    )

    sync(left, right)

    print(left)
    print(right)
    assert left.source_destination_maps == [
        SourceDestinationMap(0, 0, 50, default=True),
        SourceDestinationMap(50, 50, 50, default=True),
    ]
    assert right.source_destination_maps == [
        SourceDestinationMap(0, 0, 50, default=True),
        SourceDestinationMap(50, 0, 50, default=True),
    ]


# @pytest.mark.parametrize(
#     "split, expected",
#     [
#         (
#             [90, 109],
#             [
#                 SourceDestinationMap(100, 0, 10, default=True),
#                 SourceDestinationMap(110, 10, 90, default=True),
#             ],
#         ),
#         (
#             [150, 200],
#             [
#                 SourceDestinationMap(100, 0, 50, default=True),
#                 SourceDestinationMap(150, 50, 50, default=True),
#             ],
#         ),
#         (
#             [100, 100],
#             [
#                 SourceDestinationMap(100, 0, 1, default=True),
#                 SourceDestinationMap(101, 1, 99, default=True),
#             ],
#         ),
#         (
#             [100, 200],
#             [
#                 SourceDestinationMap(100, 0, 100, default=True),
#             ],
#         ),
#         (
#             [200, 210],
#             [
#                 SourceDestinationMap(100, 0, 100, default=True),
#             ],
#         ),
#         (
#             [190, 210],
#             [
#                 SourceDestinationMap(100, 0, 90, default=True),
#                 SourceDestinationMap(190, 90, 10, default=True),
#             ],
#         ),
#         (
#             [110, 189],
#             [
#                 SourceDestinationMap(100, 0, 10, default=True),
#                 SourceDestinationMap(110, 10, 80, default=True),
#                 SourceDestinationMap(190, 90, 10, default=True),
#             ],
#         ),
#     ],
# )
# def test_split_source(split, expected):
#     sd_map = SourceDestinationMap(100, 0, 100, default=True)
#     result = list(sd_map.split_source(*split))
#     assert result == expected


def test_insert_1():
    sd_map = SourceDestinationMap(
        source_range_start=100,
        source_range_end=200,
        destination_range_start=100,
        destination_range_end=200,
        default=True,
    )

    result = list(
        sd_map.insert(
            SourceDestinationMap(
                source_range_start=100,
                source_range_end=150,
                destination_range_start=50,
                destination_range_end=100,
            )
        )
    )
    assert result == [
        SourceDestinationMap(
            source_range_start=100,
            source_range_end=150,
            destination_range_start=50,
            destination_range_end=100,
            default=False,
        ),
        SourceDestinationMap(
            source_range_start=151,
            source_range_end=200,
            destination_range_start=151,
            destination_range_end=200,
            default=True,
        ),
    ]


def test_insert_2():
    sd_map = SourceDestinationMap(
        source_range_start=100,
        source_range_end=200,
        destination_range_start=100,
        destination_range_end=200,
        default=True,
    )

    result = list(
        sd_map.insert(
            SourceDestinationMap(
                source_range_start=150,
                source_range_end=200,
                destination_range_start=50,
                destination_range_end=100,
            )
        )
    )
    assert result == [
        SourceDestinationMap(
            source_range_start=100,
            source_range_end=149,
            destination_range_start=100,
            destination_range_end=149,
            default=True,
        ),
        SourceDestinationMap(
            source_range_start=150,
            source_range_end=200,
            destination_range_start=50,
            destination_range_end=100,
            default=False,
        ),
    ]


def test_insert_3():
    sd_map = SourceDestinationMap(
        source_range_start=100,
        source_range_end=200,
        destination_range_start=100,
        destination_range_end=200,
        default=True,
    )

    result = list(
        sd_map.insert(
            SourceDestinationMap(
                source_range_start=130,
                source_range_end=180,
                destination_range_start=50,
                destination_range_end=100,
            )
        )
    )
    assert result == [
        SourceDestinationMap(
            source_range_start=100,
            source_range_end=129,
            destination_range_start=100,
            destination_range_end=129,
            default=True,
        ),
        SourceDestinationMap(
            source_range_start=130,
            source_range_end=180,
            destination_range_start=50,
            destination_range_end=100,
            default=False,
        ),
        SourceDestinationMap(
            source_range_start=181,
            source_range_end=200,
            destination_range_start=181,
            destination_range_end=200,
            default=True,
        ),
    ]


def test_insert_4():
    sd_map = SourceDestinationMap(
        source_range_start=0,
        source_range_end=200,
        destination_range_start=0,
        destination_range_end=200,
        default=True,
    )

    result = list(
        sd_map.insert(
            SourceDestinationMap(
                source_range_start=0,
                source_range_end=10,
                destination_range_start=50,
                destination_range_end=60,
            )
        )
    )
    assert result == [
        SourceDestinationMap(
            source_range_start=0,
            source_range_end=10,
            destination_range_start=50,
            destination_range_end=60,
            default=False,
        ),
        SourceDestinationMap(
            source_range_start=11,
            source_range_end=200,
            destination_range_start=11,
            destination_range_end=200,
            default=True,
        ),
    ]


def test_insert_5():
    sd_map = SourceDestinationMap(
        source_range_start=0,
        source_range_end=200,
        destination_range_start=0,
        destination_range_end=200,
        default=True,
    )

    result = list(
        sd_map.insert(
            SourceDestinationMap(
                source_range_start=0,
                source_range_end=200,
                destination_range_start=50,
                destination_range_end=250,
            )
        )
    )
    assert result == [
        SourceDestinationMap(
            source_range_start=0,
            source_range_end=200,
            destination_range_start=50,
            destination_range_end=250,
            default=False,
        ),
    ]
