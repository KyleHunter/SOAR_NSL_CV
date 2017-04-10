import logging
from logging import FileHandler
from logging import Formatter


def setup_log():
    main_logger = logging.getLogger("SOAR.main_logger")
    main_logger.setLevel(logging.DEBUG)
    main_logger_file_handler = FileHandler("main.log")
    main_logger_file_handler.setLevel(logging.DEBUG)
    main_logger_file_handler.setFormatter(Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
    main_logger.addHandler(main_logger_file_handler)

    orientation_logger = logging.getLogger("SOAR.orientation_logger")
    orientation_logger.setLevel(logging.DEBUG)
    orientation_logger_file_handler = FileHandler("orientation.log")
    orientation_logger_file_handler.setLevel(logging.DEBUG)
    orientation_logger_file_handler.setFormatter(Formatter('%(message)s'))
    orientation_logger.addHandler(orientation_logger_file_handler)


def o_format(run_time, orientations):
    rt = "{0:.2f}".format(run_time)
    return "o1: (" + rt + ", " + str(orientations[0]) + ")\n" + \
        "o2: (" + rt + ", " + str(orientations[1]) + ")\n" + \
        "o3: (" + rt + ", " + str(orientations[2]) + ")"


# orientation_logger.info(o_format(run_time, o))

