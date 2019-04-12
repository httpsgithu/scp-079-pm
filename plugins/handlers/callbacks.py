# SCP-079-PM - Everyone can have their own Telegram private chat bot
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-PM.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import json

from pyrogram import Client

from .. import glovar
from ..functions.etc import code, thread
from ..functions.telegram import answer_callback, delete_single_message, edit_message

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_callback_query()
def answer(client, callback_query):
    try:
        aid = callback_query.from_user.id
        if aid == glovar.creator_id:
            cid = int(callback_query.message.text.partition("\n")[0].partition("ID")[2][1:])
            mid = callback_query.message.message_id
            callback_data = json.loads(callback_query.data)
            if callback_data["action"] == "recall":
                recall_mid = int(callback_data["data"])
                thread(delete_single_message, (client, cid, recall_mid))
                text = (f"发送至 ID：[{cid}](tg://user?id={cid})\n"
                        f"状态：{code('已撤回')}")
                markup = None
                thread(edit_message, (client, cid, mid, text, markup))
            else:
                answer_callback(client, callback_query.id, "")

            thread(answer_callback, (client, callback_query.id, ""))
    except Exception as e:
        logger.warning(f"Answer callback error: {e}", exc_info=True)