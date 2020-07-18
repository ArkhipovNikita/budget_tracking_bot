from actions.general import set_next_state_and_call_on_entry, ActionResult


def process_num(num: str):
    try:
        if any([sign in num for sign in '.,']):
            if ',' in num:
                num = num.replace(',', '.')
            num = float(num)
        else:
            num = int(num)
    except ValueError:
        return False, 'Please, write a number'
    if num <= 0:
        return False, 'Please, write a positive number'
    return True, num


def process_writing_sum_callback(sum_key='sum', next_state=None, next_action=None):
    @set_next_state_and_call_on_entry(next_state, next_action)
    async def process_writing_sum(query, state):
        # await sleep(0.5)
        # await query.delete()
        status, res = process_num(query.text)
        if not status:
            await query.answer(text=res)
            # await alert(query, res)
            return ActionResult.FAILED
        else:
            await state.update_data({sum_key: res})
            return ActionResult.SUCCESS
    return process_writing_sum
