import streamlit as st
import subprocess
import os
import shutil

def build_wasm():
    try:
        # Set up the environment for Emscripten
        emsdk_path = '/path/to/emsdk'
        os.environ['EMSDK'] = emsdk_path
        os.environ['EM_CONFIG'] = os.path.join(emsdk_path, '.emscripten')
        os.environ['EM_CACHE'] = os.path.join(emsdk_path, 'cache')
        os.environ['EMSDK_NODE'] = os.path.join(emsdk_path, 'node/12.18.1_64bit/bin/node')
        os.environ['EMSDK_PYTHON'] = os.path.join(emsdk_path, 'python/3.7.4_64bit/bin/python')
        os.environ['EMCC'] = os.path.join(emsdk_path, 'upstream/emscripten/emcc')

        # Run the build commands
        subprocess.run(['npm', 'install'], check=True)
        subprocess.run(['npm', 'run', 'build-release'], check=True)
        st.success("WASM module built successfully!")
    except subprocess.CalledProcessError as e:
        st.error(f"An error occurred: {e}")

def download_wasm():
    wasm_file_path = 'src/cpp/build_wasm/your_wasm_file.wasm'
    if os.path.exists(wasm_file_path):
        with open(wasm_file_path, 'rb') as f:
            st.download_button(
                label="Download WASM Module",
                data=f,
                file_name="web-ifc.wasm",
                mime="application/wasm"
            )
    else:
        st.error("WASM file not found. Please build the module first.")

st.title("Build and Download web-ifc WASM Module")
if st.button("Build WASM"):
    build_wasm()

st.write("After building, you can download the WASM module:")
download_wasm()
