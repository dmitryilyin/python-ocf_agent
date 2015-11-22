# -*- coding: utf-8 -*-
try:
    from html import escape as meta_escape
except ImportError:
    from cgi import escape as meta_escape


class MetaData(object):
    """
    The MetaData object is used to generate the meta-data XML. It will be
    used to describe this agent's capabilities to the cluster.
    """

    def __init__(self, agent):
        """
        The MetaData object required the parent Agent obeject as the first
        argument.

        :param agent: Parent Agent
        :type agent: Agent
        """
        self.agent = agent

    def show(self):
        """
        Show the meta-data XML text using the Log's output method.
        """
        self.agent.log.output(self.xml)

    @staticmethod
    def escape_string(value):
        """
        Uses html or cgi module's escape method to mask all dangerous
        characters before they are inserted to the XML.

        :param value: Input string
        :type value: str
        :return: Output string
        :rtype: str
        """
        if hasattr(value, 'replace'):
            return meta_escape(value)
        return value

    def format_line(self, offset, line, *arguments):
        """
        Format a string with offset and interpolation

        :param offset: offset width
        :type offset: int
        :param line: line template
        :type line: str
        :param arguments: template arguments
        :type arguments: list
        :return: formatted string
        :rtype: str
        """
        arguments = tuple(map(self.escape_string, arguments))
        tab = '  '
        return tab * int(offset) + line % arguments + "\n"

    @property
    def xml(self):
        """
        Generate the meta-data XML text

        :rtype: str
        :return: XML meta-data text
        """
        xml = ''
        xml += self.format_line(
            0,
            '<?xml version="1.0" encoding="%s"?>',
            self.agent.encoding
        )
        xml += self.format_line(
            0,
            '<!DOCTYPE resource-agent SYSTEM "ra-api-1.dtd">'
        )
        xml += self.format_line(
            0,
            '<resource-agent name="%s" version="%s">',
            self.agent.name,
            self.agent.version
        )
        xml += self.format_line(
            1,
            '<version>%s</version>',
            self.agent.version
        )
        xml += self.format_line(
            1,
            '<longdesc lang="%s">%s</longdesc>',
            self.agent.language,
            self.agent.long_description
        )
        xml += self.format_line(
            1,
            '<shortdesc lang="%s">%s</shortdesc>',
            self.agent.language,
            self.agent.short_description
        )

        xml += self.format_line(
            1,
            '<parameters>'
        )

        for parameter in self.agent.parameters.all.values():
            xml += self.format_line(
                2,
                '<parameter name="%s" unique="%s" required="%s">',
                parameter.name,
                int(parameter.unique),
                int(parameter.required)
            )
            xml += self.format_line(
                3,
                '<longdesc lang="%s">%s</longdesc>',
                parameter.language,
                parameter.long_description
            )
            xml += self.format_line(
                3,
                '<shortdesc lang="%s">%s</shortdesc>',
                parameter.language,
                parameter.short_description
            )
            xml += self.format_line(
                3,
                '<content type="%s" default="%s"/>',
                parameter.type_name,
                parameter.default
            )
            xml += self.format_line(
                2,
                '</parameter>'
            )

        xml += self.format_line(
            1,
            '</parameters>'
        )

        xml += self.format_line(
            1,
            '<actions>'
        )

        for handler in self.agent.handlers.all:
            line = '<action'
            for attribute_name in handler.attribute_names:
                if attribute_name in handler.attributes:
                    line += ' %s="%s"' % (
                        attribute_name,
                        self.escape_string(
                            handler.attributes[attribute_name]
                        )
                    )
            line += '/>'

            xml += self.format_line(2, line)

        xml += self.format_line(1, '</actions>')
        xml += self.format_line(
            0,
            '</resource-agent>'
        )
        return xml
