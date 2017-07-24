# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UserUpdateParameters(Model):
    """Request parameters for updating an existing work or school account user.

    :param account_enabled: Whether the account is enabled.
    :type account_enabled: bool
    :param display_name: The display name of the user.
    :type display_name: str
    :param password_profile: The password profile of the user.
    :type password_profile: :class:`PasswordProfile
     <azure.graphrbac.models.PasswordProfile>`
    :param mail_nickname: The mail alias for the user.
    :type mail_nickname: str
    """

    _attribute_map = {
        'account_enabled': {'key': 'accountEnabled', 'type': 'bool'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'password_profile': {'key': 'passwordProfile', 'type': 'PasswordProfile'},
        'mail_nickname': {'key': 'mailNickname', 'type': 'str'},
    }

    def __init__(self, account_enabled=None, display_name=None, password_profile=None, mail_nickname=None):
        self.account_enabled = account_enabled
        self.display_name = display_name
        self.password_profile = password_profile
        self.mail_nickname = mail_nickname