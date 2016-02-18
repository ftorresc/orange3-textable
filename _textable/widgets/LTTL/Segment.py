"""
Module LTTL.Segment, v0.14
Copyright 2012-2016 LangTech Sarl (info@langtech.ch)
-----------------------------------------------------------------------------
This file is part of the LTTL package v1.6.

LTTL v1.6 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LTTL v1.6 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LTTL v1.6. If not, see <http://www.gnu.org/licenses/>.
"""

from operator import itemgetter
from itertools import groupby

from .Segmentation import Segmentation


class Segment(object):
    """A class for representing components of a Segmentation."""

    __slots__ = [u'str_index', u'start', u'end', u'annotations']

    def __init__(self, str_index, start=None, end=None, annotations=None):
        """Initialize a Segment instance"""
        if annotations is None:
            annotations = dict()
        self.str_index = str_index
        self.start = start
        self.end = end
        self.annotations = annotations

    def get_content(self):
        """Stringify the content of a Segment

        :return: a string with the segment's content.
        """
        return Segmentation.data[self.str_index][self.start:self.end]

    # TODO: document parameters in docstring.
    def deepcopy(self, annotations=None, update=True):
        """Return a deep copy of the segment"""
        if update == True:
            new_annotations = self.annotations.copy()
            if annotations is not None:
                new_annotations.update(annotations)
        elif annotations is None:
            new_annotations = dict()
        else:
            new_annotations = annotations.copy()
        return Segment(
            str_index=self.str_index,
            start=self.start,
            end=self.end,
            annotations=new_annotations,
        )

    # TODO: document parameters in docstring.
    def contains(self, other_segment):
        """Test if another segment (or segment sequence) is contained in
        this one
        """
        if self.str_index != other_segment.str_index:
            return False
        if (self.start or 0) > (other_segment.start or 0):
            return False
        string_length = len(Segmentation.data[self.str_index])
        if (self.end or string_length) < (other_segment.end or string_length):
            return False
        return True

    # TODO: document parameters in docstring.
    def get_contained_segments(self, segmentation):
        """Return segments from another segmentation that are contained in
        this segment
        """
        return [
            segmentation[i] for i in self.get_contained_segment_indices(
                segmentation
            )
        ]

    # TODO: document parameters in docstring.
    def get_contained_segment_indices(self, segmentation):
        """Return indices of segments from another segmentation that are
        contained in this segment
        """
        str_index = self.str_index
        start = self.start or 0
        string_length = len(Segmentation.data[str_index])
        end = self.end or string_length
        return [
            i for i in xrange(len(segmentation)) if (
                str_index == segmentation[i].str_index and
                start <= (segmentation[i].start or 0) and
                end >= (segmentation[i].end or string_length)
            )
        ]

    # TODO: document parameters in docstring.
    def get_contained_sequence_indices(self, segmentation, length):
        """Return indices of first position of sequences of segments from
        another segmentation that are contained in this segment
        """
        contained_indices = self.get_contained_segment_indices(segmentation)
        # Find runs of consecutive contained indices
        # (cf. https://docs.python.org/2.6/library/itertools.html#examples)
        contained_idx_sequences = [
            map(itemgetter(1), g) for _, g in groupby(
                enumerate(contained_indices),
                lambda (i, x): i - x
            )
        ]
        fixed_length_idx_sequences = list()
        for contained_idx_sequence in contained_idx_sequences:
            fixed_length_idx_sequences.extend(
                [
                    contained_idx_sequence[idx] for idx in xrange(
                        len(contained_idx_sequence) - length + 1
                    )
                ]
            )
        return fixed_length_idx_sequences

# Not currently used in LTTL or Textable, nor tested.
#    def contains_sequence(self, sequence):
#        """Test if a sequence of segments is contained in this one"""
#        for other_segment in sequence:
#            if not self.contains(other_segment):
#                return False
#        return True


# Not currently used in LTTL or Textable, nor tested.
#    def equals(self, other_segment):
#        """Test if another segment has the same address as this one"""
#        return self.contains(other_segment) and other_segment.contains(self)


# Not currently used in LTTL or Textable, nor tested.
#    def get_contained_sequences(self, segmentation, length):
#        """Return sequences of segments from another segmentation that are
#        contained in this segment
#        """
#        contained_sequence_indices = self.get_contained_sequence_indices(
#            segmentation, length
#        )
#        fixed_length_sequences = [
#            segmentation[idx:idx+length] for idx in contained_sequence_indices
#        ]
#        return fixed_length_sequences
