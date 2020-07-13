from actions_lib.general import set_next_state_and_call_on_entry, ActionResult


def process_writing_desc_callback(next_state=None, next_action=None):
    @set_next_state_and_call_on_entry(next_state, next_action)
    async def process_writing_desc(query, state):
        await state.update_data(desc=query.text)
        return ActionResult.SUCCESS
    return process_writing_desc
