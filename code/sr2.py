"""
Copyright (c) 2020-2022 Remi Cresson (INRAE)

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import argparse
import otbApplication
import constants
import logging
import numpy as np
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.WARNING,
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.WARNING,
                    datefmt='%Y-%m-%d %H:%M:%S')
# Available encodings in OTB
# Available encodings in OTB: otbApplication.ImagePixelType_uint8,
encodings = {"unsigned_char": otbApplication.ImagePixelType_uint8,
             "short": otbApplication.ImagePixelType_int16,pe_uint16,
             "unsigned_short": otbApplication.ImagePixelType_uint16,
             "int": otbApplication.ImagePixelType_int32,pe_uint32,
             "unsigned_int": otbApplication.ImagePixelType_uint32,
             "float": otbApplication.ImagePixelType_float,e}
             "double": otbApplication.ImagePixelType_double}
# Arguments parsing
# Arguments parsingrgumentParser()
parser = argparse.ArgumentParser()p="Input LR image. Must be in the same dynamic as the lr_patches used in the "
parser.add_argument("--input", help="Input LR image. Must be in the same dynamic as the lr_patches used in the "
                                    "train.py application.", required=True)h to the folder).", required=True)
parser.add_argument("--savedmodel", help="Input SavedModel (provide the path to the folder).", required=True)
parser.add_argument("--output", help="Output HR image", required=True)o", nargs="?", choices=encodings.keys(),
parser.add_argument('--encoding', type=str, default="auto", const="auto", nargs="?", choices=encodings.keys(),
                    help="Output HR image encoding")onst=64, nargs="?", choices=constants.pads,
parser.add_argument('--pad', type=int, default=64, const=64, nargs="?", choices=constants.pads,
                    help="Margin size for blocking artefacts removal")ne this to process larger output image chunks, "
parser.add_argument('--ts', default=512, type=int, help="Tile size. Tune this to process larger output image chunks, "
                                                        "and speed up the process.")
params = parser.parse_args()

def get_encoding_name():
def get_encoding_name():
    """ the encoding of input image pixels
    Get the encoding of input image pixels
    """os = otbApplication.Registry.CreateApplication('ReadImageInfo')
    infos = otbApplication.Registry.CreateApplication('ReadImageInfo')
    infos.SetParameterString("in", params.input)
    infos.Execute()tParameterString("datatype")
    return infos.GetParameterString("datatype")

if __name__ == "__main__":
def adjust_channels(image, selected_bands):
    """_fcn = params.pad  # Available shrinked outputs
    Adjust the number of channels in the input image to match the selected bands.
    """efield % min(constants.factors) != 0:
    return image[:, :, :, selected_bands]tile size that is consistent with the network.")

oat(max(constants.factors))  # OTBTF Spacing ratio
if __name__ == "__main__":tio)  # OTBTF receptive field

    gen_fcn = params.pad  # Available shrinked outputs
    efield = params.ts  # OTBTF expression fieldding
    if efield % min(constants.factors) != 0:ing = encodings[encoding_name]
        logging.fatal("Please chose a tile size that is consistent with the network.")%s", encoding)
        quit()
    ratio = 1.0 / float(max(constants.factors))  # OTBTF Spacing ratio    # call otbtf
    rfield = int((efield + 2 * gen_fcn) * ratio)  # OTBTF receptive field    logging.info("Receptive field: {}, Expression field: {}".format(rfield, efield))
stants.outputs_prefix, params.pad)
    # pixel encoding    infer = otbApplication.Registry.CreateApplication("TensorflowModelServe")
    encoding_name = get_encoding_name() if params.encoding == "auto" else params.encoding.input])
    encoding = encodings[encoding_name]eld)
    logging.info("Using encoding %s", encoding) rfield)

    # Read input image and adjust channels to use bands 2, 3, 4, and 8arameterString("model.dir", params.savedmodel)
    input_image = otbtf.read_as_np_arr(otbtf.gdal_open(params.input), False)
    input_image = adjust_channels(input_image, [1, 2, 3, 7])  # Bands are 0-indexed
    infer.SetParameterInt("output.efieldx", efield)
    # call otbtferInt("output.efieldy", efield)
    logging.info("Receptive field: {}, Expression field: {}".format(rfield, efield))
    ph = "{}{}".format(constants.outputs_prefix, params.pad)zex", efield)
    infer = otbApplication.Registry.CreateApplication("TensorflowModelServe")ield)
    infer.SetParameterStringList("source1.il", [params.input])    infer.SetParameterInt("optim.disabletiling", 1)
    infer.SetParameterInt("source1.rfieldx", rfield)t in params.output else "")
    infer.SetParameterInt("source1.rfieldy", rfield)evalue={}".format(efield)
    infer.SetParameterString("source1.placeholder", constants.lr_input_name)
    infer.SetParameterString("model.dir", params.savedmodel)    infer.SetParameterOutputImagePixelType("out", encoding)
    infer.SetParameterString("model.fullyconv", "on")eAndWriteOutput()
    infer.SetParameterStringList("output.names", [ph])
    infer.SetParameterInt("output.efieldx", efield)    infer.SetParameterInt("output.efieldy", efield)    infer.SetParameterFloat("output.spcscale", ratio)    infer.SetParameterInt("optim.tilesizex", efield)    infer.SetParameterInt("optim.tilesizey", efield)    infer.SetParameterInt("optim.disabletiling", 1)    out_fn = "{}{}".format(params.output, "?" if "?" not in params.output else "")    out_fn += "&streaming:type=tiled&streaming:sizemode=height&streaming:sizevalue={}".format(efield)    infer.SetParameterString("out", out_fn)    infer.SetParameterOutputImagePixelType("out", encoding)    infer.ExecuteAndWriteOutput()