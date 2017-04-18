from re import sub


def delete_break_line(s):
    return sub("\n", ' ', s)


class Project:

    def __init__(self, name, status, inherit_categories, view_status, description):
        self.name = name
        self.status = status
        self.inherit_categories = inherit_categories
        self.view_status = view_status
        self.description = description

    def __repr__(self):
        return '%s,%s' % (self.name, delete_break_line(self.description))

    def __eq__(self, other):
        return (self.name == other.name
                and delete_break_line(self.description) == delete_break_line(other.description)
                and self.inherit_categories == other.inherit_categories
                and self.view_status == other.view_status
                and self.status == other.status
                )

    def get_name(self):
        return self.name


