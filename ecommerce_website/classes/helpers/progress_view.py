def get_order_progress_phases(current_status=None):
    # Define the phases
    phases = [
        {'name': 'Openstaand', 'status': 'open'},
        {'name': 'Betaald', 'status': 'paid'},
        {'name': 'Wachtende op bezorgservice', 'status': 'partly'},
        {'name': 'Geleverd', 'status': 'delivered'}
    ]

    if current_status:
        status_found = False  # Track if the current status is found

        for i, phase in enumerate(phases):
            if phase['status'] == current_status:
                if current_status == 'delivered':
                    # If it's 'delivered', mark it as completed
                    phase['status'] = 'completed'
                elif current_status in ['open', 'failed'] and i == 0:
                    # If it's the first phase and is 'open' or 'failed', make it current
                    phase['status'] = 'current'
                else:
                    # Mark this phase as the current phase
                    phase['status'] = 'current'
                status_found = True
            elif status_found:
                # Mark all subsequent phases as 'upcoming'
                phase['status'] = 'upcoming'
            else:
                # Mark all previous phases as 'completed'
                phase['status'] = 'completed'
    else:
        # Default logic if `current_status` is not provided
        for i, phase in enumerate(phases):
            if i == 0:
                phase['status'] = 'current'
            else:
                phase['status'] = 'upcoming'

    return phases


def get_return_progress_phases(current_status=None):
    # Define the phases
    phases = [
        {'name': 'Openstaand', 'status': 'open'},
        {'name': 'Betaald', 'status': 'paid'},
        {'name': 'Wachtende op bezorgservice', 'status': 'partly'},
        {'name': 'Opgehaald', 'status': 'delivered'},
        {'name': 'Afgerond', 'status': 'done'}

    ]

    if current_status:
        status_found = False  # Track if the current status is found

        for i, phase in enumerate(phases):
            if phase['status'] == current_status:
                if current_status == 'done':
                    # If it's 'delivered', mark it as completed
                    phase['status'] = 'completed'
                elif current_status in ['open', 'failed'] and i == 0:
                    # If it's the first phase and is 'open' or 'failed', make it current
                    phase['status'] = 'current'
                else:
                    # Mark this phase as the current phase
                    phase['status'] = 'current'
                status_found = True
            elif status_found:
                # Mark all subsequent phases as 'upcoming'
                phase['status'] = 'upcoming'
            else:
                # Mark all previous phases as 'completed'
                phase['status'] = 'completed'
    else:
        # Default logic if `current_status` is not provided
        for i, phase in enumerate(phases):
            if i == 0:
                phase['status'] = 'current'
            else:
                phase['status'] = 'upcoming'

    return phases
