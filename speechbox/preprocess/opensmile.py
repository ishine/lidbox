"""
Subprocess wrapper over the SMILExtract binary from the openSMILE toolkit.
"""
import os

import numpy as np

import speechbox.system as system


def speech_dataset_to_features(labels, paths, opensmile_conf_path, label_to_index, tmpdir):
    smilextract_cmd = (
        "SMILExtract -nologfile"
        " -configfile " + opensmile_conf_path
        + " -I {path} -O {tmpout}"
    )
    for i, (label, wavpath) in enumerate(zip(labels, paths), start=1):
        tmpout = os.path.join(tmpdir, "{label}-{i}.arff".format(label=label, i=i))
        system.run_command(smilextract_cmd.format(path=wavpath, tmpout=tmpout))
        feats, feat_names = system.read_arff_features(tmpout)
        if feats.ndim == 2 and feats.shape[0] == 1 and feats.size == feats.shape[1]:
            feats = feats.reshape(-1)
        os.remove(tmpout)
        onehot = np.zeros(len(label_to_index), dtype=np.float32)
        onehot[label_to_index[label]] = 1.0
        yield feats, onehot, feat_names