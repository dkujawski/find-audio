import argparse
import os
import torchaudio
import torch
import numpy as np
import csv

def load_audio_fft(file_path):
    waveform, sample_rate = torchaudio.load(file_path)
    mono_waveform = waveform.mean(dim=0)  # Convert to mono if needed
    fft_values = torch.fft.fft(mono_waveform).abs()
    return fft_values, sample_rate

def find_matching_segments(ref_fft, target_fft, sample_rate, threshold=0.9):
    ref_len = len(ref_fft)
    target_len = len(target_fft)
    matches = []
    
    for i in range(target_len - ref_len + 1):
        segment = target_fft[i:i+ref_len]
        similarity = torch.cosine_similarity(ref_fft, segment, dim=0)
        if similarity.mean().item() >= threshold:
            matches.append(i / sample_rate)  # Convert to time in seconds
    
    return matches

def process_target_file(ref_fft, ref_sr, target_path, output_file):
    target_fft, target_sr = load_audio_fft(target_path)
    if target_sr != ref_sr:
        print(f"Skipping {target_path}: Sample rate mismatch ({target_sr} != {ref_sr})")
        return
    
    matches = find_matching_segments(ref_fft, target_fft, target_sr)
    
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        for match in matches:
            writer.writerow([os.path.basename(target_path), match])

def main():
    parser = argparse.ArgumentParser(description="Find occurrences of a reference audio in target files using FFT.")
    parser.add_argument("reference", type=str, help="Path to the reference audio file.")
    parser.add_argument("target", type=str, help="Path to a target audio file or directory.")
    parser.add_argument("--output", type=str, default="output.csv", help="CSV file to store results.")
    
    args = parser.parse_args()
    
    ref_fft, ref_sr = load_audio_fft(args.reference)
    
    if os.path.isdir(args.target):
        for file in os.listdir(args.target):
            if file.endswith(".wav"):
                process_target_file(ref_fft, ref_sr, os.path.join(args.target, file), args.output)
    else:
        process_target_file(ref_fft, ref_sr, args.target, args.output)
    
    print(f"Results saved in {args.output}")

if __name__ == "__main__":
    main()

