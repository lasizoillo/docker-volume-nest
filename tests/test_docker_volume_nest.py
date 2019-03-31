import datetime

import pytest
from hamcrest import (all_of, assert_that, contains_string, greater_than,
                      has_entries, is_, smaller_than)


class TestExample(object):
    def test_it_should_have_same_value(self):
        first = 'value'
        second = 'value'

        assert_that(first, is_(second))

    def test_it_should_contain_personal_details(self):
        data = {
            'name': 'My name',
            'age': 30,
            'test': 20,
        }

        assert_that(data, has_entries(
            name=contains_string('name'),
            age=all_of(greater_than(20), smaller_than(40))
        ))

    def test_it_should_validate_dates(self):
        bad_date = '32-13-2019'

        with pytest.raises(ValueError):
            datetime.datetime.strptime(bad_date, '%d-%m-%Y')

    def test_it_should_create_files(self, tmpdir):
        pass
