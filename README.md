<h1>Immunofluorescence-tif2nifti</h1>
<p>Template pipeline to convert outputs of immunofluorescence microscopy tif z-stack outputs to NIfTI format, with the option to save as 3D RGB or 2D RGB projection.</p>
<h2>Installation</h2>
<p>To install the required dependencies, use the <code>requirements.txt</code> file:</p>
<pre><code>pip3 install -r requirements.txt</code></pre>
<h2>Example Usage</h2>
<pre><code>python /path_to_file/t2n.py "path_to_target_folder/" "path_to_output_folder/" "subject_file_ID" --mode "proj"</code></pre>
<p>In this example, replace <code>/path_to_file/t2n.py</code> with the actual path to the script, <code>"path_to_target_folder/"</code> with the path to the folder containing the <code>.tif</code> files, <code>"path_to_output_folder/"</code> with the desired output folder, and <code>"subject_file_ID"</code> with the sample ID. Use <code>--mode "proj"</code> to save the output as a 2D RGB projection.</p>
