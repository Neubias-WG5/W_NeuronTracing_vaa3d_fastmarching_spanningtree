import sys
import os
import glob
from subprocess import call
from cytomine.models import Job
from neubiaswg5 import CLASS_TRETRC
from neubiaswg5.helpers import NeubiasJob, prepare_data, upload_data, upload_metrics
from workflow import workflow 

def main(argv):
    # 0. Initialize Cytomine client and job
    with NeubiasJob.from_cli(argv) as nj:
        nj.job.update(status=Job.RUNNING, progress=0, statusComment="Initialisation...")
        problem_cls = CLASS_TRETRC
        is_2d = False
        
        # 1. Create working directories on the machine
        # 2. Download the images
        in_images, gt_images, in_path, gt_path, out_path, tmp_path = prepare_data(problem_cls, nj, is_2d=is_2d, **nj.flags)
        
        # 3. Call the image analysis workflow using the run script
        nj.job.update(progress=25, statusComment="Launching workflow...")
        workflow(in_images, out_path)
        #if return_code != 0:
        #   err_desc = "Failed to execute the Vaa3D (return code: {})".format(return_code)
        #nj.job.update(progress=50, statusComment=err_desc)
        #    raise ValueError(err_desc)       
        print('files in out_path '+ out_path +': ')
        for file in glob.glob(out_path+'/*'):
            print(file)

        #files = (glob.glob(in_path+"/*.tif"))
        #print('Removing flipped images...')
        #for i in range(0,len(files)):
        #    files[i] = files[i].replace('/in/','/out/')
        #    print(files[i])
        #for out_file in files:
        #    os.remove(out_file)
       
        # 4. Upload the annotation and labels to Cytomine (annotations are extracted from the mask using
        # the AnnotationExporter module
        upload_data(problem_cls, nj, in_images, out_path, **nj.flags, projection=-1, is_2d=is_2d, monitor_params={
            "start": 60, "end": 90,
            "period": 0.1,
            "prefix": "Extracting and uploading polygons from masks"
        })
        
        #5. Compute and upload the metrics
        nj.job.update(progress=80, statusComment="Computing and uploading metrics (if necessary)...")
        upload_metrics(problem_cls, nj, in_images, gt_path, out_path, tmp_path, **nj.flags)
        nj.job.update(status=Job.TERMINATED, progress=100, statusComment="Finished.")

if __name__ == "__main__":
    main(sys.argv[1:])

