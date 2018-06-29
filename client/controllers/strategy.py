from client import controllers


def controller_choice(controller=None, precon_interpreter=None,
                      interpreter=None, standby=None, reboot=False, **kwargs):

    step = None
    easy_choose = {
        'controller_for_cam':           controllers.ControllerForCAM,
        'controller_standby_Mediaset':  controllers.ControllerStandbyMediaset,
        'controller_with_precondition': controllers.ControllerWithPrecondition,
        'controller_with_tv_standby':   controllers.ControllerWithTVStandby,
        'controller_with_tvreboot':     controllers.ControllerWithTVReboot,
        'controller_standard':          controllers.ControllerStandard,
        'get_service_list':             controllers.ControllerForTVServiceList,
        'clear_crashes_dumps':          controllers.ControllerForClearCrashesDumps,
        'download_crashes_dumps':       controllers.ControllerForDownloadCrashesDumps,
        'get_serial_logs':              controllers.ControllerForSerialLogs,
        'check_inet_from_tv':           controllers.ControllerForCheckInetFromTV,
        'for_timeout':                  controllers.ControllerTimeout,
        'for_ci_plus_auth':             controllers.ControllerForCIPlusAuth,
        'for_ci_plus_nightdcm':         controllers.ControllerForCIPlusNightDCM,
        'get_tv_screenshot':            controllers.ControllerGetTVScreenshot,
        'delete_key':                   controllers.ControllerDeleteKeys,
        'start_lstreamer':              controllers.ControllerStartLstreamer,
    }

    if controller and controller != 'universal':
        step = easy_choose.get(controller)
    else:
        if ((precon_interpreter and interpreter) is not None and
                standby is None and not reboot):
            step = controllers.ControllerWithPrecondition

        elif (precon_interpreter is None and standby is not None and
              not reboot):
            step = controllers.ControllerWithTVStandby

        elif ((precon_interpreter and standby) is None and reboot):
            step = controllers.ControllerWithTVReboot

        elif ((precon_interpreter and standby) is None and
              interpreter is not None and not reboot):
            step = controllers.ControllerStandard

        elif ((precon_interpreter and standby and interpreter) is None and
              not reboot):
            step = controllers.ControllerForPlayback

    if not step:
        raise RuntimeError(
            'Test was not started. Controller was not defined correctly'
        )
    return step
