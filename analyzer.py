from helper_func import *
from settings import *

check_valid_num_log_files()

create_dirs(DETAILS_RESULT_PATH)

analyse_phase_1()
analyse_phase_2()
analyse_phase_3()

output_result()
