"""
First level analysis of localizer dataset
=========================================
Full step-by-step example of fitting a GLM to experimental data and visualizing
the results.
More specifically:
1. A sequence of fMRI volumes are loaded
2. A design matrix describing all the effects related to the data is computed
3. a mask of the useful brain volume is computed
4. A GLM is applied to the dataset (effect/covariance,
   then contrast estimation)
"""
import numpy as np
import pandas as pd
from nilearn import plotting

from nistats.first_level_model import FirstLevelModel

#########################################################################
# Prepare data and analysis parameters
# -------------------------------------
# Prepare timing
t_r = 0.955
slice_time_ref = t_r / 12

# Prepare data
paradigm_file = "/hpc/banco/bastien.c/data/inter_tva/sub-01/paradigms/" \
                "usub-01_task-localizer-best_bold.tsv"
paradigm = pd.read_csv(paradigm_file, sep='\t', index_col=None)
fmri_img = "/hpc/banco/InterTVA/virginia/analyse_pilot/sub-01/" \
           "func/session1/swusub-01_task-localizer-best_bold.nii"
output = "/hpc/banco/bastien.c/data/inter_tva/sub-01/output/" \
         "swusub-01_localizer-best_bold_nistat_ex/con"

#########################################################################
# Perform first level analysis
# ----------------------------
# Setup and fit GLM
first_level_model = FirstLevelModel(t_r, slice_time_ref,
                                    hrf_model='glover + derivative', verbose=2)
first_level_model = first_level_model.fit(fmri_img, paradigm)

#########################################################################
# Estimate contrasts
# ------------------
# Specify the contrasts
design_matrix = first_level_model.design_matrices_[0]
contrast_matrix = np.eye(design_matrix.shape[1])
contrasts = dict([(column, contrast_matrix[i])
                  for i, column in enumerate(design_matrix.columns)])

#########################################################################
# Short list of more relevant contrasts
contrasts = {
    "all_minus_silence": (contrasts["speech"] + contrasts["non_speech"]
            + contrasts["emotional"] + contrasts["environmental"]
            + contrasts["animal"] + contrasts['artificial']),
    "voice_minus_nvoice": (contrasts["speech"] + contrasts["non_speech"]
            + contrasts["emotional"] - contrasts["environmental"]
            - contrasts["animal"] - contrasts['artificial'])
    }

#########################################################################
# contrast estimation
for index, (contrast_id, contrast_val) in enumerate(contrasts.items()):
    print('  Contrast % 2i out of %i: %s' %
          (index + 1, len(contrasts), contrast_id))
    z_map = first_level_model.compute_contrast(contrast_val,
                                               output_type='stat')
    z_map.to_filename(output + "_" + contrast_id)
    # Create snapshots of the contrasts
    display = plotting.plot_stat_map(z_map, display_mode='z', title=contrast_id)

plotting.show()


# """
# First level analysis of localizer dataset
# =========================================
#
# Full step-by-step example of fitting a GLM to experimental data and visualizing
# the results.
#
# More specifically:
#
# 1. A sequence of fMRI volumes are loaded
# 2. A design matrix describing all the effects related to the data is computed
# 3. a mask of the useful brain volume is computed
# 4. A GLM is applied to the dataset (effect/covariance,
#    then contrast estimation)
#
# """
# from os import mkdir, path
#
# import numpy as np
# import pandas as pd
# from nilearn import plotting
#
# from nistats.first_level_model import FirstLevelModel
# from nistats import datasets
#
# #########################################################################
# # Prepare data and analysis parameters
# # -------------------------------------
# # Prepare timing
# t_r = 0.955#2.4
# slice_time_ref = t_r/12#0.5
#
# # Prepare data
# #data = datasets.fetch_localizer_first_level()
# #paradigm_file = data.paradigm
# paradigm_file = "/hpc/banco/bastien.c/data/inter_tva/sub-01/paradigms/" \
#                  "usub-01_task-localizer-best_bold.tsv"
# paradigm = pd.read_csv(paradigm_file, sep='\t', index_col=None)
# #paradigm = pd.read_csv(paradigm_file, sep=' ', header=None, index_col=None)
# #paradigm.columns = ['session', 'trial_type', 'onset']
# #fmri_img = data.epi_img
# fmri_img = "/hpc/banco/InterTVA/virginia/analyse_pilot/sub-01/" \
#             "func/session1/usub-01_task-localizer-best_bold.nii"
#
# #########################################################################
# # Perform first level analysis
# # ----------------------------
# # Setup and fit GLM
# first_level_model = FirstLevelModel(t_r, slice_time_ref, drift_model="blank",
#                                     hrf_model='glover + derivative')
# first_level_model = first_level_model.fit(fmri_img, paradigm)
#
# #########################################################################
# # Estimate contrasts
# # ------------------
# # Specify the contrasts
# design_matrix = first_level_model.design_matrices_[0]
# contrast_matrix = np.eye(design_matrix.shape[1])
# contrasts = dict([(column, contrast_matrix[i])
#                   for i, column in enumerate(design_matrix.columns)])
#
# # contrasts["audio"] = contrasts["clicDaudio"] + contrasts["clicGaudio"] +\
# #     contrasts["calculaudio"] + contrasts["phraseaudio"]
# # contrasts["video"] = contrasts["clicDvideo"] + contrasts["clicGvideo"] + \
# #     contrasts["calculvideo"] + contrasts["phrasevideo"]
# # contrasts["computation"] = contrasts["calculaudio"] + contrasts["calculvideo"]
# # contrasts["sentences"] = contrasts["phraseaudio"] + contrasts["phrasevideo"]
# #
# # #########################################################################
# # # Short list of more relevant contrasts
# # contrasts = {
# #     "left-right": (contrasts["clicGaudio"] + contrasts["clicGvideo"]
# #                    - contrasts["clicDaudio"] - contrasts["clicDvideo"]),
# #     "H-V": contrasts["damier_H"] - contrasts["damier_V"],
# #     "audio-video": contrasts["audio"] - contrasts["video"],
# #     "video-audio": -contrasts["audio"] + contrasts["video"],
# #     "computation-sentences": (contrasts["computation"] -
# #                               contrasts["sentences"]),
# #     "reading-visual": contrasts["phrasevideo"] - contrasts["damier_H"]
# #     }
#
# #########################################################################
# # contrast estimation
# for index, (contrast_id, contrast_val) in enumerate(contrasts.items()):
#     print('  Contrast % 2i out of %i: %s' %
#           (index + 1, len(contrasts), contrast_id))
#     z_map = first_level_model.compute_contrast(contrast_val,
#                                                output_type='stat')
#
#     # Create snapshots of the contrasts
#     display = plotting.plot_stat_map(z_map, display_mode='z', title=contrast_id)
#
# plotting.show()
