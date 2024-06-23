#!/usr/bin/env python3
# -*- coding: utf-8 -*-

signal1 = [-267.46, -214.19, -162.45, -124.81, -114.8, -104.95, -93.13, -74.74, -50.44, -24.83, 8.66, 48.73, 75.65, 133.53, 173.32, 214.71, 264.85, 259.27, 216.3, 173.32, 133.53, 101.7, 100.1, 93.74, 83.39, 67.48, 49.97, 51.56, 53.15, 51.56, 51.56, 53.15, 49.97, 38.83, 20.52, 3.01, -16.09, -32.8, -47.12, -56.68, -63.84, -68.61, -65.43, -60.65, -50.31, -38.37, -24.84, -8.93, 3.81, 19.73, 36.44, 36.44, 20.52, 1.42, 11.77, 34.05, 53.15, 74.64, 92.14, 104.09, 112.04, 113.63, 97.72, 79.42, 57.13, 32.46, 3.01, -18.47, -40.76, -60.65, -72.59, -82.94, -92.1, -112.39, -101.24, -86.85, -78.16, -90.1, -90.1, -82.94, -71.0, -59.06, -39.96, -17.68, 5.4, 33.26, 57.92, 81.01, 99.31, 114.43, 139.1, 161.38, 176.5, 187.65, 200.98, 205.01, 207.23, 200.98, 189.08, 176.06, 173.99, 177.43, 185.66, 193.88, 189.77, 180.16, 174.68, 176.06, 154.11, 118.45, 93.08, 56.74, 32.05, 35.36, 47.14, 59.48, 71.83, 72.52, 48.52, 32.05, 24.33, 14.41, -4.31, -24.15, -23.05, -20.84, -28.01, -29.11, -29.66, -26.9, -28.01, -29.66, -28.56, -21.95, -12.03, -4.31, 0.09, 0.65, 3.4, 2.29, 0.09, -7.62, -14.23, -21.95, -23.05, -24.15, -47.84, -64.92, -84.76, -80.35, -71.53, -60.51, -45.64, -23.05, 1.75, 24.88, 36.46, 36.46, 34.8, 30.4, 24.88, 13.31, -3.76, -23.6, -47.84, -66.2, -88.28, -107.28, -126.28, -149.89, -148.55, -144.5, -131.01, -115.49, -88.52, -76.38, -58.17, -75.03, -91.22, -116.17, -133.7, -139.1, -145.17, -143.15, -140.44, -132.35, -132.35, -128.31, -124.94, -103.36, -82.45, -85.15, -102.68, -118.87, -131.68, -130.34, -124.94, -136.4, -151.24, -164.73, -179.56, -195.75, -201.48, -210.82, -226.78, -219.36, -210.59, -194.4, -176.19, -158.66, -171.47, -185.63, -199.12, -211.27, -199.8, -185.63, -168.1, -149.21, -128.98, -128.31, -124.94, -108.07, -85.15, -81.1, -94.59, -110.77, -131.01, -149.89, -164.73, -180.24, -195.08, -211.94, -223.4, -233.52, -238.91, -236.9, -232.84, -219.36, -196.42, -175.09, -156.2, -141.12, -155.02, -156.64, -153.94, -151.91, -147.87, -161.35, -176.19, -194.4, -204.52, -207.89, -208.57, -198.45, -183.62, -169.45, -155.96, -156.42, -153.76, -148.43, -142.03, -133.5, -128.17, -145.76, -163.35, -171.88, -164.95, -161.22, -163.35, -172.42, -184.68, -180.94, -173.48, -171.35, -170.29, -177.22, -187.88, -180.94, -176.68, -175.08, -157.01, -155.35, -153.23, -147.89, -143.09, -135.63, -128.7, -146.3, -171.88, -200.67, -227.86, -243.32, -259.23]

signal2 = [216.38, 212.3, 211.43, 211.43, 232.07, 249.81, 266.23, 278.7, 277.39, 257.69, 231.42, 197.92, 197.26, 196.02, 197.61, 203.18, 212.73, 210.34, 201.59, 196.02, 196.02, 193.63, 168.96, 149.86, 140.31, 136.34, 136.34, 149.06, 172.94, 195.23, 185.67, 161.0, 136.34, 141.1, 149.06, 159.41, 173.74, 186.47, 196.81, 198.41, 185.67, 168.96, 176.92, 192.83, 199.2, 190.45, 180.1, 170.55, 162.59, 151.45, 142.69, 122.0, 122.0, 123.6, 122.81, 122.0, 120.41, 117.23, 113.25, 102.11, 87.79, 71.86, 78.23, 84.6, 86.99, 87.79, 87.79, 83.01, 79.03, 67.09, 48.79, 29.68, 5.59, 5.02, 5.02, 2.61, -2.94, 3.43, 11.38, 31.28, 48.79, 67.89, 79.03, 84.6, 89.38, 88.58, 86.99, 83.01, 77.44, 69.48, 55.16, 32.87, 12.18, -9.31, -40.49, -61.05, -78.58, -91.08, -99.6, -103.72, -85.89, -69.44, -50.92, -33.09, -42.01, -62.58, -83.14, -103.03, -105.09, -109.2, -113.32, -114.69, -114.0, -124.55, -131.15, -131.15, -124.97, -113.32, -114.0, -113.32, -124.55, -139.43, -135.02, -128.4, -116.28, -104.72, -94.25, -79.92, -61.19, -44.11, -54.02, -71.66, -93.69, -104.16, -104.16, -94.79, -82.12, -68.9, -53.47, -62.84, -81.02, -99.2, -105.81, -106.36, -115.73, -127.85, -120.14, -111.32, -99.75, -79.36, -50.72, -25.93, -11.05, -11.05, -22.07, -36.95, -58.43, -75.51, -93.14, -112.43, -125.65, -139.97, -135.02, -128.4, -120.69, -148.24, -190.55, -227.94, -255.53, -289.25, -258.23, -235.3, -225.19, -209.0, -190.78, -169.21, -132.11, -134.14, -140.88, -159.09, -169.21, -193.49, -232.6, -220.46, -192.81, -146.95, -126.05, -92.32, -73.44, -82.21, -89.62, -100.42, -108.51, -117.95, -126.05, -105.14, -74.78, -63.32, -53.2, -41.74, -45.11, -45.11, -51.53, -52.24, -47.8, -57.92, -61.97, -70.74, -74.78, -76.13, -86.93, -91.65, -92.32, -88.28, -99.07, -107.16, -111.88, -113.9, -107.16, -90.3, -71.41, -81.53, -90.3, -78.16, -69.39, -56.57, -41.74, -27.58, -41.06, -45.79, -44.44, -29.59, -12.06, 7.49, 29.75, 53.36, 76.97, 89.78, 91.12, 88.09, 81.36, 78.31, 81.16, 60.77, 39.2, 21.66, 6.15, -1.27, -8.02, -1.95, 13.57, 30.43, 48.64, 62.12, 64.15, 62.8, 62.12, 83.72, 113.05, 138.64, 161.56, 189.28, 207.94, 209.01, 209.54, 207.94, 195.15, 177.56, 161.56, 167.95, 173.82, 161.56, 147.16, 134.9, 122.11, 126.91, 131.18, 115.18, 101.32, 87.99, 81.59, 101.32, 118.38, 139.17, 162.62, 185.02, 206.34, 208.48, 210.08, 210.61, 211.14, 210.61, 212.58]

signal3 = [-75.24, -62.72, -50.2, -37.6, -24.91, -12.21, 0.5, 13.27, 26.07, 38.9, 51.74, 63.87, 64.11, 59.43, 63.27, 54.97, 46.31, 49.24, 56.43, 69.34, 75.86, 77.22, 78.58, 79.94, 81.3, 82.66, 84.04, 85.47, 86.9, 88.33, 89.76, 91.19, 92.62, 91.7, 90.28, 88.85, 87.42, 85.99, 89.09, 101.99, 114.89, 118.46, 117.46, 106.12, 99.36, 100.36, 110.12, 123.02, 133.75, 132.67, 131.59, 130.51, 129.43, 128.35, 127.27, 138.4, 151.22, 164.04, 176.86, 189.68, 202.5, 190.95, 178.13, 165.31, 152.49, 139.66, 127.07, 123.45, 129.0, 124.54, 118.37, 110.95, 102.02, 91.57, 80.06, 67.8, 55.16, 42.32, 29.43, 16.6, 3.92, -8.51, -20.42, -31.86, -41.12, -46.04, -55.83, -68.5, -71.92, -83.2, -86.76, -94.51, -86.95, -75.4, -63.73, -51.9, -39.81, -27.35, -14.67, -1.91, 10.9, 23.75, 36.65, 49.52, 62.29, 74.92, 87.34, 99.51, 111.35, 122.81, 133.82, 144.33, 154.26, 163.45, 171.8, 179.22, 185.66, 191.07, 195.44, 198.76, 201.03, 202.19, 198.62, 193.35, 191.0, 188.4, 184.34, 178.82, 172.37, 165.34, 157.71, 149.16, 139.73, 129.5, 118.6, 107.14, 95.24, 83.0, 70.5, 57.83, 45.04, 32.17, 19.27, 6.42, -6.31, -18.89, -31.31, -43.56, -55.63, -67.52, -79.2, -87.01, -83.41, -72.27, -60.53, -48.58, -36.43, -24.1, -11.61, 1.03, 13.79, 26.64, 39.54, 52.43, 65.22, 77.82, 90.1, 101.91, 113.24, 124.0, 134.06, 143.31, 151.68, 159.08, 165.47, 170.83, 175.15, 178.39, 180.45, 171.51, 166.69, 163.03, 158.32, 152.61, 145.9, 138.18, 129.51, 119.91, 109.48, 98.34, 86.62, 74.44, 61.94, 49.21, 36.35, 23.44, 10.58, -2.16, -14.73, -27.06, -39.13, -50.87, -62.24, -68.45, -60.58, -49.11, -37.76, -25.97, -13.83, -1.4, 11.27, 24.1, 37.01, 49.87, 62.56, 74.95, 86.95, 98.45, 109.31, 119.35, 128.43, 136.39, 143.13, 148.57, 152.62, 155.06, 142.81, 140.15, 135.59, 129.3, 121.54, 112.56, 102.59, 91.85, 80.51, 68.55, 56.05, 43.24, 30.33, 17.5, 4.86, -7.54, -19.62, -31.36, -42.66, -41.23, -43.18, -50.52, -62.37, -70.12, -69.41, -78.72, -91.18, -96.25, -85.5, -85.88, -92.98, -103.34, -115.58, -128.23, -139.26, -147.71, -135.87, -129.23, -140.2, -152.46, -165.32, -177.7, -188.44, -196.86, -202.7, -204.82, -202.36, -195.89, -186.16, -174.39, -166.91, -160.24, -170.28, -172.39, -167.0, -156.78, -144.04, -151.89, -162.75, -163.53, -161.0, -154.05, -143.68, -131.25, -118.42, -106.36, -96.43, -89.07, -85.65, -87.87, -93.63, -96.82, -89.3, -85.85, -75.4, -67.24, -73.43, -73.11, -60.85, -49.85, -42.7, -40.35, -33.74, -22.25, -10.31, 2.0, 14.6, 27.4, 40.3, 53.16, 65.85, 78.16, 89.78, 100.38, 109.66, 117.43, 123.6, 128.1, 125.06, 134.55, 147.35, 160.16, 172.96, 185.76, 198.56, 209.99, 202.99, 200.45, 197.92, 195.39, 192.85, 190.32, 189.07, 201.88, 205.91, 209.35, 209.39, 205.36, 201.34, 191.49, 178.6, 170.25, 170.47, 170.69, 168.33, 155.43, 142.53, 129.63, 116.72, 103.83, 91.02, 79.05, 79.1, 76.84, 77.71, 90.61, 103.5, 116.4, 129.3, 142.21, 155.11, 168.0, 180.89, 193.78, 203.27, 209.67, 216.07, 222.46, 228.86, 235.26, 231.27, 218.42, 205.57, 192.72, 182.63, 177.56, 172.44, 172.94, 171.57, 162.76, 150.11, 140.34, 130.39, 122.74, 110.54, 99.94, 95.77, 96.8, 89.3, 78.65, 74.11, 66.85, 57.16, 45.68, 33.21, 20.34, 7.8, -3.43, -12.72, -19.88, -12.62, -0.71, 11.19, 20.77, 18.09, 13.93, 9.77, 12.48, 16.63, 20.79, 31.1, 37.45, 42.85, 48.26, 45.17, 39.77, 34.37, 39.19, 51.42, 63.64, 75.87, 66.81, 54.58, 42.35, 39.32, 48.95, 60.55, 72.14, 65.04, 53.45, 41.85, 32.29, 36.65, 41.01, 45.37, 41.43, 37.06, 32.7, 21.14, 15.27, 9.67, 4.06, 8.72, 14.31, 19.91, 14.27, 16.39, 27.54, 37.79, 38.89, 29.3, 17.67, 8.09, -3.91, -15.92, -23.79, -26.47, -24.44, -20.03, -13.17, -3.72, 7.55, 19.97, 32.78, 45.19, 56.74, 66.58, 74.2, 78.67, 79.31, 77.75, 73.62, 66.56, 56.76, 45.09, 32.52, 19.65, 7.13, -4.0, -13.02, -19.82, -24.5, -27.88, -31.27, -34.67, -38.06, -41.45, -44.84, -48.24, -51.63, -55.02, -58.42, -61.81, -65.63, -75.24, -68.98, -62.72, -56.46, -50.2, -43.93, -37.6, -31.25, -24.91, -18.56, -12.21, -5.87, 0.5, 6.88, 13.27, 19.67, 26.07, 32.48, 38.9, 45.31, 51.74, 58.19, 63.87, 64.95, 64.11, 58.04, 59.43, 63.08, 63.27, 61.04, 54.97, 48.89, 46.31, 47.78, 49.24, 50.71, 56.43, 62.89, 69.34, 75.18, 75.86, 76.54, 77.22, 77.9, 78.58, 79.26, 79.94, 80.62, 81.3, 81.98, 82.66, 83.34, 84.04, 84.75, 85.47, 86.18, 86.9, 87.61, 88.33, 89.04, 89.76, 90.47, 91.19, 91.9, 92.62, 92.42, 91.7, 90.99, 90.28, 89.56, 88.85, 88.13, 87.42, 86.71, 85.99, 85.28, 89.09, 95.54, 101.99, 108.44, 114.89, 118.96, 118.46, 117.96, 117.46, 112.57, 106.12, 99.67, 99.36, 99.86, 100.36, 103.67, 110.12, 116.57, 123.02, 129.47, 133.75, 133.21, 132.67, 132.13, 131.59, 131.05, 130.51, 129.97, 129.43, 128.89, 128.35, 127.81, 127.27, 131.99, 138.4, 144.81, 151.22, 157.63, 164.04, 170.45, 176.86, 183.27, 189.68, 196.09, 202.5, 197.36, 190.95, 184.54, 178.13, 171.72, 165.31, 158.9, 152.49, 146.08, 139.66, 133.25, 127.07, 125.26, 123.45, 129.68, 129.0, 127.05, 124.54, 121.62, 118.37, 114.83, 110.95, 106.69, 102.02, 96.96, 91.57, 85.93, 80.06, 74.0, 67.8, 61.52, 55.16, 48.76, 42.32, 35.87, 29.43, 23.0, 16.6, 10.24, 3.92, -2.33, -8.51, -14.54, -20.42, -26.19, -31.86, -37.44, -41.12, -43.07, -46.04, -50.29, -55.83, -62.07, -68.5, -68.85, -71.92, -77.13, -83.2, -84.43, -86.76, -90.15, -94.51, -92.68, -86.95, -81.19, -75.4, -69.58, -63.73, -57.84, -51.9, -45.9, -39.81, -33.62, -27.35, -21.03, -14.67, -8.3, -1.91, 4.49, 10.9, 17.32, 23.75, 30.2, 36.65, 43.09, 49.52, 55.92, 62.29, 68.63, 74.92, 81.16, 87.34, 93.46, 99.51, 105.47, 111.35, 117.13, 122.81, 128.37, 133.82, 139.14, 144.33, 149.38, 154.26, 158.96, 163.45, 167.74, 171.8, 175.63, 179.22, 182.56, 185.66, 188.49, 191.07, 193.38, 195.44, 197.23, 198.76, 200.03, 201.03, 201.76, 202.19, 202.29, 198.62, 193.61, 193.35, 192.32, 191.0, 189.8, 188.4, 186.59, 184.34, 181.73, 178.82, 175.69, 172.37, 168.91, 165.34, 161.64, 157.71, 153.55, 149.16, 144.55, 139.73, 134.71, 129.5, 124.13, 118.6, 112.94, 107.14, 101.24, 95.24, 89.15, 83.0, 76.77, 70.5, 64.18, 57.83, 51.44, 45.04, 38.61, 32.17, 25.72, 19.27, 12.83, 6.42, 0.04, -6.31, -12.62, -18.89, -25.12, -31.31, -37.46, -43.56, -49.62, -55.63, -61.59, -67.52, -73.38, -79.2, -84.95, -87.01, -84.67, -83.41, -78.04, -72.27, -66.43, -60.53, -54.58, -48.58, -42.53, -36.43, -30.29, -24.1, -17.88, -11.61, -5.31, 1.03, 7.39, 13.79, 20.2, 26.64, 33.09, 39.54, 45.99, 52.43, 58.84, 65.22, 71.56, 77.82, 84.01, 90.1, 96.07, 101.91, 107.64, 113.24, 118.7, 124.0, 129.12, 134.06, 138.79, 143.31, 147.61, 151.68, 155.5, 159.08, 162.4, 165.47, 168.28, 170.83, 173.12, 175.15, 176.91, 178.39, 179.59, 180.45, 177.91, 171.51, 168.07, 166.69, 165.0, 163.03, 160.8, 158.32, 155.59, 152.61, 149.38, 145.9, 142.16, 138.18, 133.96, 129.51, 124.82, 119.91, 114.79, 109.48, 104.0, 98.34, 92.54, 86.62, 80.58, 74.44, 68.22, 61.94, 55.6, 49.21, 42.79, 36.35, 29.9, 23.44, 17.0, 10.58, 4.19, -2.16, -8.47, -14.73, -20.93, -27.06, -33.13, -39.13, -45.04, -50.87, -56.61, -62.24, -67.73, -68.45, -67.0, -60.58, -54.57, -49.11, -43.5, -37.76, -31.91, -25.97, -19.95, -13.83, -7.65, -1.4, 4.91, 11.27, 17.67, 24.1, 30.55, 37.01, 43.45, 49.87, 56.24, 62.56, 68.8, 74.95, 81.0, 86.95, 92.77, 98.45, 103.97, 109.31, 114.44, 119.35, 124.03, 128.43, 132.56, 136.39, 139.92, 143.13, 146.02, 148.57, 150.77, 152.62, 154.08, 155.06, 149.2, 142.81, 141.67, 140.15, 138.11, 135.59, 132.64, 129.3, 125.59, 121.54, 117.19, 112.56, 107.69, 102.59, 97.31, 91.85, 86.25, 80.51, 74.62, 68.55, 62.35, 56.05, 49.67, 43.24, 36.79, 30.33, 23.9, 17.5, 11.15, 4.86, -1.38, -7.54, -13.62, -19.62, -25.54, -31.36, -37.07, -42.66, -43.1, -41.23, -41.16, -43.18, -46.24, -50.52, -56.1, -62.37, -68.67, -70.12, -68.47, -69.41, -73.23, -78.72, -84.94, -91.18, -95.89, -96.25, -91.64, -85.5, -83.95, -85.88, -88.93, -92.98, -97.86, -103.34, -109.27, -115.58, -122.01, -128.23, -134.0, -139.26, -144.0, -147.71, -141.66, -135.87, -130.53, -129.23, -134.53, -140.2, -146.2, -152.46, -158.88, -165.32, -171.64, -177.7, -183.36, -188.44, -192.94, -196.86, -200.16, -202.7, -204.31, -204.82, -204.15, -202.36, -199.59, -195.89, -191.36, -186.16, -180.46, -174.39, -170.88, -166.91, -161.43, -160.24, -165.83, -170.28, -172.61, -172.39, -170.29, -167.0, -162.47, -156.78, -150.44, -144.04, -145.46, -151.89, -158.15, -162.75, -163.5, -163.53, -162.75, -161.0, -158.09, -154.05, -149.2, -143.68, -137.63, -131.25, -124.8, -118.42, -112.22, -106.36, -101.04, -96.43, -92.41, -89.07, -86.67, -85.65, -86.17, -87.87, -90.17, -93.63, -98.74, -96.82, -92.36, -89.3, -87.04, -85.85, -81.42, -75.4, -70.5, -67.24, -67.78, -73.43, -79.44, -73.11, -66.9, -60.85, -55.09, -49.85, -45.63, -42.7, -41.0, -40.35, -39.24, -33.74, -28.06, -22.25, -16.33, -10.31, -4.2, 2.0, 8.26, 14.6, 20.98, 27.4, 33.84, 40.3, 46.74, 53.16, 59.54, 65.85, 72.07, 78.16, 84.07, 89.78, 95.22, 100.38, 105.2, 109.66, 113.74, 117.43, 120.72, 123.6, 126.07, 128.1, 129.65, 125.06, 128.15, 134.55, 140.95, 147.35, 153.75, 160.16, 166.56, 172.96, 179.36, 185.76, 192.16, 198.56, 204.97, 209.99, 206.31, 202.99, 201.72, 200.45, 199.19, 197.92, 196.65, 195.39, 194.12, 192.85, 191.58, 190.32, 189.05, 189.07, 195.48, 201.88, 204.19, 205.91, 207.63, 209.35, 211.07, 209.39, 207.38, 205.36, 203.35, 201.34, 197.93, 191.49, 185.04, 178.6, 172.16, 170.25, 170.36, 170.47, 170.58, 170.69, 172.52, 168.33, 161.88, 155.43, 148.98, 142.53, 136.08, 129.63, 123.18, 116.72, 110.27, 103.83, 97.41, 91.02, 84.66, 79.05, 79.27, 79.1, 78.37, 76.84, 74.74, 77.71, 84.16, 90.61, 97.05, 103.5, 109.95, 116.4, 122.85, 129.3, 135.76, 142.21, 148.66, 155.11, 161.55, 168.0, 174.45, 180.89, 187.33, 193.78, 200.07, 203.27, 206.47, 209.67, 212.87, 216.07, 219.27, 222.46, 225.66, 228.86, 232.06, 235.26, 237.69, 231.27, 224.84, 218.42, 211.99, 205.57, 199.14, 192.72, 186.29, 182.63, 180.1, 177.56, 175.03, 172.44, 170.74, 172.94, 173.38, 171.57, 168.02, 162.76, 156.45, 150.11, 144.46, 140.34, 136.38, 130.39, 127.6, 122.74, 116.93, 110.54, 104.65, 99.94, 96.77, 95.77, 96.95, 96.8, 95.64, 89.3, 82.95, 78.65, 76.74, 74.11, 70.81, 66.85, 62.28, 57.16, 51.6, 45.68, 39.52, 33.21, 26.79, 20.34, 13.97, 7.8, 1.97, -3.43, -8.34, -12.72, -16.58, -19.88, -18.57, -12.62, -6.67, -0.71, 5.24, 11.19, 16.04, 20.77, 20.17, 18.09, 16.01, 13.93, 11.85, 9.77, 10.4, 12.48, 14.56, 16.63, 18.71, 20.79, 24.83, 31.1, 34.75, 37.45, 40.15, 42.85, 45.55, 48.26, 47.87, 45.17, 42.47, 39.77, 37.07, 34.37, 35.28, 39.19, 45.3, 51.42, 57.53, 63.64, 69.76, 75.87, 72.93, 66.81, 60.7, 54.58, 48.47, 42.35, 39.65, 39.32, 43.15, 48.95, 54.75, 60.55, 66.35, 72.14, 70.84, 65.04, 59.25, 53.45, 47.65, 41.85, 37.19, 32.29, 34.47, 36.65, 38.83, 41.01, 43.19, 45.37, 43.61, 41.43, 39.25, 37.06, 34.88, 32.7, 27.41, 21.14, 18.07, 15.27, 12.47, 9.67, 6.87, 4.06, 5.92, 8.72, 11.52, 14.31, 17.11, 19.91, 17.03, 14.27, 14.05, 16.39, 21.3, 27.54, 33.41, 37.79, 39.81, 38.89, 35.02, 29.3, 22.93, 17.67, 14.09, 8.09, 2.09, -3.91, -9.91, -15.92, -21.56, -23.79, -25.56, -26.47, -25.8, -24.44, -22.52, -20.03, -16.93, -13.17, -8.76, -3.72, 1.75, 7.55, 13.65, 19.97, 26.41, 32.78, 39.07, 45.19, 51.11, 56.74, 61.96, 66.58, 70.65, 74.2, 77.02, 78.67, 79.25, 79.31, 78.82, 77.75, 76.03, 73.62, 70.46, 66.56, 61.96, 56.76, 51.09, 45.09, 38.87, 32.52, 26.09, 19.65, 13.28, 7.13, 1.33, -4.0, -8.79, -13.02, -16.69, -19.82, -22.43, -24.5, -26.18, -27.88, -29.58, -31.27, -32.97, -34.67, -36.36, -38.06, -39.75, -41.45, -43.15, -44.84, -46.54, -48.24, -49.93, -51.63, -53.33, -55.02, -56.72, -58.42, -60.11, -61.81, -63.51, -65.63, -70.43]

signal4 = [-9.28, -12.38, -15.55, -18.3, -20.65, -22.99, -25.25, -27.1, -28.73, -30.21, -31.52, -32.9, -43.33, -44.71, -56.43, -57.54, -51.28, -38.71, -31.67, -32.04, -25.1, -12.27, 0.57, 13.4, 26.24, 39.07, 51.91, 64.74, 77.57, 90.39, 103.22, 116.05, 128.88, 120.65, 107.83, 95.0, 82.17, 69.34, 60.68, 61.04, 61.41, 52.89, 40.02, 38.71, 44.63, 57.5, 61.22, 61.64, 60.01, 47.15, 34.28, 21.42, 8.56, -4.3, -17.17, -17.41, -15.92, -14.42, -12.93, -11.43, -9.94, -11.28, -12.78, -14.27, -15.77, -17.27, -19.03, -31.42, -36.87, -48.96, -60.29, -70.84, -80.14, -87.68, -93.5, -97.53, -100.1, -101.32, -101.01, -99.54, -97.13, -93.67, -88.72, -82.75, -80.34, -92.21, -100.3, -102.0, -113.8, -119.69, -131.92, -142.15, -148.56, -154.32, -159.84, -164.99, -169.53, -172.86, -175.31, -177.25, -178.82, -180.04, -180.09, -179.14, -177.31, -174.64, -171.15, -166.83, -161.7, -155.75, -149.02, -141.53, -133.3, -124.24, -114.4, -103.84, -92.66, -80.94, -68.8, -56.33, -43.63, -30.78, -21.94, -30.24, -42.93, -55.57, -67.81, -79.48, -90.65, -101.47, -111.89, -121.55, -130.35, -138.23, -145.13, -151.07, -156.04, -160.12, -163.35, -165.8, -167.53, -168.53, -168.37, -167.13, -165.01, -162.13, -158.62, -154.55, -149.98, -144.95, -139.47, -132.47, -120.14, -125.47, -130.84, -135.7, -140.06, -143.88, -147.14, -149.77, -151.71, -152.88, -153.19, -152.56, -150.89, -148.09, -144.11, -138.93, -132.76, -125.63, -117.55, -108.56, -98.73, -88.16, -76.95, -65.21, -53.05, -40.56, -27.82, -25.43, -35.62, -48.0, -60.01, -71.59, -82.6, -92.95, -102.5, -111.12, -118.72, -125.23, -130.61, -134.89, -138.09, -140.21, -141.23, -141.19, -140.13, -138.09, -135.15, -131.36, -126.77, -121.43, -115.31, -106.71, -101.79, -104.39, -110.52, -115.78, -120.17, -123.62, -126.07, -127.41, -127.59, -126.53, -124.21, -120.63, -115.86, -110.01, -103.05, -94.96, -85.79, -75.64, -64.64, -52.94, -40.69, -28.03, -29.14, -41.5, -53.57, -64.82, -75.13, -84.39, -92.58, -99.73, -105.89, -110.72, -113.89, -115.42, -115.43, -114.08, -111.53, -107.92, -103.4, -98.03, -91.8, -80.82, -86.87, -97.34, -101.97, -97.33, -109.86, -118.33, -118.59, -113.88, -120.03, -130.19, -140.88, -148.49, -152.32, -150.39, -143.8, -134.64, -129.58, -125.02, -131.77, -135.69, -135.99, -132.52, -125.46, -115.72, -104.25, -91.58, -78.98, -67.87, -59.48, -54.29, -63.05, -67.02, -59.2, -46.82, -35.2, -27.65, -27.32, -26.64, -29.78, -16.92, -4.31, 6.45, 14.02, 17.15, 16.1, 11.64, 3.49, -7.07, -19.4, -32.04, -43.49, -46.3, -36.01, -23.64, -23.01, -32.69, -38.92, -38.93, -42.92, -49.57, -60.17, -72.8, -81.92, -87.81, -92.7, -96.58, -99.36, -100.96, -101.3, -100.32, -97.99, -94.12, -88.53, -81.19, -72.24, -61.95, -50.62, -38.54, -31.37, -30.16, -28.52, -26.88, -25.24, -23.59, -21.95, -19.7, -8.95, 3.71, 16.37, 29.03, 41.68, 54.34, 66.07, 67.67, 79.43, 91.87, 104.23, 116.5, 128.76, 132.47, 131.72, 135.7, 148.61, 161.51, 163.23, 162.79, 162.35, 161.95, 162.01, 162.71, 164.2, 166.05, 153.15, 140.48, 131.86, 131.29, 130.75, 130.26, 129.86, 129.96, 130.47, 131.1, 131.81, 132.56, 138.79, 150.0, 161.21, 172.42, 183.63, 194.85, 199.35, 198.13, 196.91, 195.7, 190.7, 178.83, 167.29, 177.99, 190.57, 199.58, 199.64, 191.67, 188.45, 198.36, 201.43, 194.54, 182.62, 170.06, 164.82, 169.17, 181.22, 191.85, 200.33, 206.17, 209.39, 209.91, 207.03, 200.75, 191.83, 181.12, 174.35, 169.36, 164.37, 169.16, 180.75, 192.97, 205.19, 197.23, 185.01, 172.79, 169.54, 178.25, 189.98, 201.7, 195.0, 183.28, 171.56, 161.57, 165.71, 169.85, 173.98, 170.92, 166.79, 162.65, 152.3, 145.84, 140.17, 134.5, 137.97, 143.64, 149.31, 144.22, 132.07, 119.92, 107.77, 118.76, 130.91, 143.06, 143.56, 132.77, 121.14, 109.51, 119.17, 130.81, 142.44, 152.96, 165.32, 170.63, 163.43, 151.08, 143.1, 146.38, 148.33, 143.58, 138.84, 143.46, 156.04, 168.76, 180.87, 191.77, 200.5, 206.73, 210.11, 209.45, 205.95, 200.24, 191.96, 181.57, 169.54, 156.67, 143.87, 131.67, 120.91, 112.58, 107.14, 104.28, 104.0, 106.98, 113.43, 122.62, 133.56, 145.57, 136.07, 123.62, 111.16, 98.71, 86.26, 73.8, 61.35, 48.89, 36.44, 23.98, 11.53, -0.66, -9.28, -10.82, -12.38, -13.95, -15.55, -17.04, -18.3, -19.49, -20.65, -21.82, -22.99, -24.18, -25.25, -26.21, -27.1, -27.93, -28.73, -29.48, -30.21, -30.91, -31.52, -31.77, -32.9, -39.26, -43.33, -41.14, -44.71, -50.04, -56.43, -59.72, -57.54, -55.36, -51.28, -45.0, -38.71, -32.43, -31.67, -31.85, -32.04, -31.52, -25.1, -18.69, -12.27, -5.85, 0.57, 6.98, 13.4, 19.82, 26.24, 32.66, 39.07, 45.49, 51.91, 58.32, 64.74, 71.15, 77.57, 83.98, 90.39, 96.81, 103.22, 109.64, 116.05, 122.47, 128.88, 127.07, 120.65, 114.24, 107.83, 101.41, 95.0, 88.58, 82.17, 75.75, 69.34, 62.93, 60.68, 60.86, 61.04, 61.23, 61.41, 59.33, 52.89, 46.46, 40.02, 38.49, 38.71, 38.92, 44.63, 51.07, 57.5, 61.0, 61.22, 61.43, 61.64, 61.86, 60.01, 53.58, 47.15, 40.71, 34.28, 27.85, 21.42, 14.99, 8.56, 2.13, -4.3, -10.74, -17.17, -18.16, -17.41, -16.67, -15.92, -15.17, -14.42, -13.68, -12.93, -12.18, -11.43, -10.68, -9.94, -10.54, -11.28, -12.03, -12.78, -13.53, -14.27, -15.02, -15.77, -16.52, -17.27, -18.01, -19.03, -25.22, -31.42, -30.79, -36.87, -43.01, -48.96, -54.71, -60.29, -65.69, -70.84, -75.69, -80.14, -84.14, -87.68, -90.82, -93.5, -95.71, -97.53, -98.98, -100.1, -100.89, -101.32, -101.34, -101.01, -100.39, -99.54, -98.45, -97.13, -95.55, -93.67, -91.37, -88.72, -85.83, -82.75, -79.5, -80.34, -86.49, -92.21, -97.04, -100.3, -101.89, -102.0, -108.21, -113.8, -117.57, -119.69, -125.91, -131.92, -137.39, -142.15, -145.59, -148.56, -151.47, -154.32, -157.12, -159.84, -162.47, -164.99, -167.37, -169.53, -171.35, -172.86, -174.16, -175.31, -176.33, -177.25, -178.08, -178.82, -179.49, -180.04, -180.21, -180.09, -179.73, -179.14, -178.33, -177.31, -176.08, -174.64, -173.0, -171.15, -169.09, -166.83, -164.37, -161.7, -158.83, -155.75, -152.48, -149.02, -145.37, -141.53, -137.52, -133.3, -128.87, -124.24, -119.42, -114.4, -109.21, -103.84, -98.32, -92.66, -86.86, -80.94, -74.92, -68.8, -62.6, -56.33, -50.0, -43.63, -37.22, -30.78, -24.32, -21.94, -23.81, -30.24, -36.61, -42.93, -49.27, -55.57, -61.77, -67.81, -73.71, -79.48, -85.12, -90.65, -96.1, -101.47, -106.76, -111.89, -116.82, -121.55, -126.06, -130.35, -134.41, -138.23, -141.8, -145.13, -148.22, -151.07, -153.67, -156.04, -158.19, -160.12, -161.84, -163.35, -164.67, -165.8, -166.75, -167.53, -168.15, -168.53, -168.6, -168.37, -167.87, -167.13, -166.17, -165.01, -163.66, -162.13, -160.45, -158.62, -156.65, -154.55, -152.32, -149.98, -147.52, -144.95, -142.27, -139.47, -136.55, -132.47, -126.47, -120.14, -122.58, -125.47, -128.22, -130.84, -133.33, -135.7, -137.94, -140.06, -142.04, -143.88, -145.59, -147.14, -148.54, -149.77, -150.83, -151.71, -152.39, -152.88, -153.15, -153.19, -153.0, -152.56, -151.86, -150.89, -149.64, -148.09, -146.25, -144.11, -141.66, -138.93, -135.97, -132.76, -129.31, -125.63, -121.7, -117.55, -113.16, -108.56, -103.74, -98.73, -93.53, -88.16, -82.63, -76.95, -71.14, -65.21, -59.18, -53.05, -46.84, -40.56, -34.22, -27.82, -24.6, -25.43, -29.32, -35.62, -41.85, -48.0, -54.06, -60.01, -65.86, -71.59, -77.17, -82.6, -87.87, -92.95, -97.83, -102.5, -106.93, -111.12, -115.06, -118.72, -122.12, -125.23, -128.06, -130.61, -132.89, -134.89, -136.63, -138.09, -139.29, -140.21, -140.86, -141.23, -141.35, -141.19, -140.79, -140.13, -139.23, -138.09, -136.73, -135.15, -133.36, -131.36, -129.16, -126.77, -124.19, -121.43, -118.47, -115.31, -111.92, -106.71, -102.13, -101.79, -100.96, -104.39, -107.57, -110.52, -113.26, -115.78, -118.09, -120.17, -122.02, -123.62, -124.98, -126.07, -126.88, -127.41, -127.65, -127.59, -127.22, -126.53, -125.53, -124.21, -122.57, -120.63, -118.38, -115.86, -113.08, -110.01, -106.67, -103.05, -99.14, -94.96, -90.5, -85.79, -80.83, -75.64, -70.24, -64.64, -58.87, -52.94, -46.88, -40.69, -34.41, -28.03, -28.3, -29.14, -35.23, -41.5, -47.62, -53.57, -59.31, -64.82, -70.1, -75.13, -79.89, -84.39, -88.62, -92.58, -96.28, -99.73, -102.93, -105.89, -108.51, -110.72, -112.51, -113.89, -114.85, -115.42, -115.61, -115.43, -114.92, -114.08, -112.94, -111.53, -109.85, -107.92, -105.77, -103.4, -100.81, -98.03, -95.03, -91.8, -86.99, -80.82, -80.74, -86.87, -92.54, -97.34, -100.52, -101.97, -101.8, -97.33, -103.53, -109.86, -114.98, -118.33, -119.91, -118.59, -114.27, -113.88, -118.31, -120.03, -124.04, -130.19, -135.87, -140.88, -145.1, -148.49, -151.04, -152.32, -152.08, -150.39, -147.53, -143.8, -139.42, -134.64, -132.41, -129.58, -125.95, -125.02, -128.71, -131.77, -134.14, -135.69, -136.32, -135.99, -134.72, -132.52, -129.43, -125.46, -120.84, -115.72, -110.18, -104.25, -98.01, -91.58, -85.17, -78.98, -73.15, -67.87, -63.29, -59.48, -56.47, -54.29, -58.01, -63.05, -66.43, -67.02, -63.83, -59.2, -53.24, -46.82, -40.73, -35.2, -30.62, -27.65, -26.6, -27.32, -26.88, -26.64, -28.08, -29.78, -23.37, -16.92, -10.52, -4.31, 1.43, 6.45, 10.71, 14.02, 16.25, 17.15, 17.03, 16.1, 14.33, 11.64, 8.0, 3.49, -1.55, -7.07, -13.05, -19.4, -25.82, -32.04, -38.07, -43.49, -47.34, -46.3, -41.68, -36.01, -29.97, -23.64, -20.87, -23.01, -27.18, -32.69, -38.97, -38.92, -37.67, -38.93, -40.67, -42.92, -45.81, -49.57, -54.43, -60.17, -66.38, -72.8, -78.56, -81.92, -84.99, -87.81, -90.38, -92.7, -94.77, -96.58, -98.11, -99.36, -100.31, -100.96, -101.3, -101.3, -100.98, -100.32, -99.32, -97.99, -96.27, -94.12, -91.55, -88.53, -85.07, -81.19, -76.9, -72.24, -67.25, -61.95, -56.4, -50.62, -44.66, -38.54, -32.28, -31.37, -30.98, -30.16, -29.34, -28.52, -27.7, -26.88, -26.06, -25.24, -24.41, -23.59, -22.77, -21.95, -21.13, -19.7, -14.4, -8.95, -2.62, 3.71, 10.04, 16.37, 22.7, 29.03, 35.35, 41.68, 48.01, 54.34, 60.67, 66.07, 66.87, 67.67, 73.21, 79.43, 85.65, 91.87, 98.09, 104.23, 110.37, 116.5, 122.63, 128.76, 132.85, 132.47, 132.1, 131.72, 131.35, 135.7, 142.16, 148.61, 155.06, 161.51, 166.97, 163.23, 163.01, 162.79, 162.57, 162.35, 162.13, 161.95, 161.9, 162.01, 162.27, 162.71, 163.34, 164.2, 165.32, 166.05, 159.6, 153.15, 146.74, 140.48, 134.37, 131.86, 131.57, 131.29, 131.02, 130.75, 130.5, 130.26, 130.04, 129.86, 129.81, 129.96, 130.19, 130.47, 130.78, 131.1, 131.45, 131.81, 132.18, 132.56, 133.19, 138.79, 144.4, 150.0, 155.61, 161.21, 166.82, 172.42, 178.03, 183.63, 189.24, 194.85, 199.96, 199.35, 198.74, 198.13, 197.52, 196.91, 196.3, 195.7, 195.09, 190.7, 184.76, 178.83, 172.89, 167.29, 171.96, 177.99, 184.41, 190.57, 195.92, 199.58, 200.69, 199.64, 196.59, 191.67, 187.95, 188.45, 194.14, 198.36, 201.12, 201.43, 198.91, 194.54, 188.96, 182.62, 176.3, 170.06, 163.71, 164.82, 165.95, 169.17, 175.33, 181.22, 186.76, 191.85, 196.4, 200.33, 203.59, 206.17, 208.09, 209.39, 210.04, 209.91, 208.91, 207.03, 204.28, 200.75, 196.56, 191.83, 186.66, 181.12, 176.85, 174.35, 171.86, 169.36, 166.86, 164.37, 164.87, 169.16, 174.64, 180.75, 186.86, 192.97, 199.08, 205.19, 203.34, 197.23, 191.12, 185.01, 178.9, 172.79, 170.58, 169.54, 172.39, 178.25, 184.11, 189.98, 195.84, 201.7, 200.87, 195.0, 189.14, 183.28, 177.42, 171.56, 166.49, 161.57, 163.64, 165.71, 167.78, 169.85, 171.92, 173.98, 172.99, 170.92, 168.86, 166.79, 164.72, 162.65, 158.69, 152.3, 148.67, 145.84, 143.0, 140.17, 137.33, 134.5, 135.13, 137.97, 140.8, 143.64, 146.48, 149.31, 148.23, 144.22, 138.14, 132.07, 126.0, 119.92, 113.85, 107.77, 112.69, 118.76, 124.83, 130.91, 136.98, 143.06, 142.67, 143.56, 138.59, 132.77, 126.96, 121.14, 115.33, 109.51, 113.36, 119.17, 124.99, 130.81, 136.62, 142.44, 147.16, 152.96, 159.36, 165.32, 169.4, 170.63, 168.13, 163.43, 157.42, 151.08, 146.02, 143.1, 142.83, 146.38, 150.7, 148.33, 145.96, 143.58, 141.21, 138.84, 137.41, 143.46, 149.66, 156.04, 162.45, 168.76, 174.92, 180.87, 186.53, 191.77, 196.48, 200.5, 203.91, 206.73, 208.84, 210.11, 210.39, 209.45, 207.98, 205.95, 203.39, 200.24, 196.45, 191.96, 186.95, 181.57, 175.77, 169.54, 163.12, 156.67, 150.23, 143.87, 137.66, 131.67, 126.05, 120.91, 116.4, 112.58, 109.51, 107.14, 105.42, 104.28, 103.77, 104.0, 105.05, 106.98, 109.8, 113.43, 117.74, 122.62, 127.92, 133.56, 139.46, 145.57, 142.3, 136.07, 129.84, 123.62, 117.39, 111.16, 104.94, 98.71, 92.48, 86.26, 80.03, 73.8, 67.57, 61.35, 55.12, 48.89, 42.67, 36.44, 30.21, 23.98, 17.76, 11.53, 5.3, -0.66, -4.97]

test8_signal1 = [0.00000000e+00,  6.26666168e+00,  1.24344944e+01,  1.84062276e+01,
        2.40876837e+01,  2.93892626e+01,  3.42273553e+01,  3.85256621e+01,
        4.22163963e+01,  4.52413526e+01,  4.75528258e+01,  4.91143625e+01,
        4.99013364e+01,  4.99013364e+01,  4.91143625e+01,  4.75528258e+01,
        4.52413526e+01,  4.22163963e+01,  3.85256621e+01,  3.42273553e+01,
        2.93892626e+01,  2.40876837e+01,  1.84062276e+01,  1.24344944e+01,
        6.26666168e+00, -1.60812265e-14, -6.26666168e+00, -1.24344944e+01,
       -1.84062276e+01, -2.40876837e+01, -2.93892626e+01, -3.42273553e+01,
       -3.85256621e+01, -4.22163963e+01, -4.52413526e+01, -4.75528258e+01,
       -4.91143625e+01, -4.99013364e+01, -4.99013364e+01, -4.91143625e+01,
       -4.75528258e+01, -4.52413526e+01, -4.22163963e+01, -3.85256621e+01,
       -3.42273553e+01, -2.93892626e+01, -2.40876837e+01, -1.84062276e+01,
       -1.24344944e+01, -6.26666168e+00,  3.21624530e-14,  6.26666168e+00,
        1.24344944e+01,  1.84062276e+01,  2.40876837e+01,  2.93892626e+01,
        3.42273553e+01,  3.85256621e+01,  4.22163963e+01,  4.52413526e+01,
        4.75528258e+01,  4.91143625e+01,  4.99013364e+01,  4.99013364e+01,
        4.91143625e+01,  4.75528258e+01,  4.52413526e+01,  4.22163963e+01,
        3.85256621e+01,  3.42273553e+01,  2.93892626e+01,  2.40876837e+01,
        1.84062276e+01,  1.24344944e+01,  6.26666168e+00,  1.83697020e-14,
       -6.26666168e+00, -1.24344944e+01, -1.84062276e+01, -2.40876837e+01,
       -2.93892626e+01, -3.42273553e+01, -3.85256621e+01, -4.22163963e+01,
       -4.52413526e+01, -4.75528258e+01, -4.91143625e+01, -4.99013364e+01,
       -4.99013364e+01, -4.91143625e+01, -4.75528258e+01, -4.52413526e+01,
       -4.22163963e+01, -3.85256621e+01, -3.42273553e+01, -2.93892626e+01,
       -2.40876837e+01, -1.84062276e+01, -1.24344944e+01, -6.26666168e+00]

test8_signal2 = [ 5.00000000e+01,  4.99013364e+01,  4.96057351e+01,  4.91143625e+01,
        4.84291581e+01,  4.75528258e+01,  4.64888243e+01,  4.52413526e+01,
        4.38153340e+01,  4.22163963e+01,  4.04508497e+01,  3.85256621e+01,
        3.64484314e+01,  3.42273553e+01,  3.18711995e+01,  2.93892626e+01,
        2.67913397e+01,  2.40876837e+01,  2.12889646e+01,  1.84062276e+01,
        1.54508497e+01,  1.24344944e+01,  9.36906573e+00,  6.26666168e+00,
        3.13952598e+00, -8.04061325e-15, -3.13952598e+00, -6.26666168e+00,
       -9.36906573e+00, -1.24344944e+01, -1.54508497e+01, -1.84062276e+01,
       -2.12889646e+01, -2.40876837e+01, -2.67913397e+01, -2.93892626e+01,
       -3.18711995e+01, -3.42273553e+01, -3.64484314e+01, -3.85256621e+01,
       -4.04508497e+01, -4.22163963e+01, -4.38153340e+01, -4.52413526e+01,
       -4.64888243e+01, -4.75528258e+01, -4.84291581e+01, -4.91143625e+01,
       -4.96057351e+01, -4.99013364e+01, -5.00000000e+01, -4.99013364e+01,
       -4.96057351e+01, -4.91143625e+01, -4.84291581e+01, -4.75528258e+01,
       -4.64888243e+01, -4.52413526e+01, -4.38153340e+01, -4.22163963e+01,
       -4.04508497e+01, -3.85256621e+01, -3.64484314e+01, -3.42273553e+01,
       -3.18711995e+01, -2.93892626e+01, -2.67913397e+01, -2.40876837e+01,
       -2.12889646e+01, -1.84062276e+01, -1.54508497e+01, -1.24344944e+01,
       -9.36906573e+00, -6.26666168e+00, -3.13952598e+00, -9.18485099e-15,
        3.13952598e+00,  6.26666168e+00,  9.36906573e+00,  1.24344944e+01,
        1.54508497e+01,  1.84062276e+01,  2.12889646e+01,  2.40876837e+01,
        2.67913397e+01,  2.93892626e+01,  3.18711995e+01,  3.42273553e+01,
        3.64484314e+01,  3.85256621e+01,  4.04508497e+01,  4.22163963e+01,
        4.38153340e+01,  4.52413526e+01,  4.64888243e+01,  4.75528258e+01,
        4.84291581e+01,  4.91143625e+01,  4.96057351e+01,  4.99013364e+01]