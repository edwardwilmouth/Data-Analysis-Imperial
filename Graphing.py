import pandas as pd
from ipyvizzu import Chart, Data, Config, Style, DisplayTarget
import os
import shutil
import time
import imageio.v2 as imageio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
 
def ChartCreation(): 
    # initialize Chart    
    # add data to Chart
    '''
    GENERAL FORMAT

    chart = Chart(
        width="640px", height="360px", display=DisplayTarget.MANUAL
    )
    data = Data()
    csv = input("CSV Filename: ")
    df = pd.read_csv(
        csv
    )
    data.add_df(df)
    
    chart.animate(data)
    
    x_data = ["Joy factors", "Country"]  # data group(s) to put on x axis
    y_data = "Value 5 (+/-)"  # data group(s) to put on y axis

    # add config to Chart
    chart.animate(
        Config(
            {
                "channels": {
                    "x": x_data,
                    "y": y_data,
                    "color": "Joy factors",
                    "label": "Value 5 (+/-)",
                },
                "title": "Grouped Column Chart",
            }
        ),
        Style(
            {
                "plot": {
                    "marker": {
                        "label": {
                            "fontSize": 6,
                            "orientation": "vertical",
                            "angle": -3.14,
                        }
                    }
                }
            }
        ),
    )
    '''

    
    # SPECIFIC FOR LCOE

    df = pd.read_csv(
        r"C:\Users\...\LCOE All - IEA.csv"
    )

    '''
    FORMAT CHANGE TO DECADE IF NECESSARY

    grouped_data = df.groupby(df['year'] // 10 * 10)['average'].mean().reset_index()
    # Rename the columns if needed
    grouped_data.columns = ['Decade', 'Average']
    #grouped_data['Month Name'] = df['month_name'].copy()
    
    #grouped_data['Month Name'] = grouped_data['Month Name'].astype(str)
    print(grouped_data)
    '''

    df['LCOE (USD/MWh)'] = df['LCOE (USD/MWh)'].astype(str)
    data = Data()
    data.add_df(df)
    
    chart = Chart(
        width="640px", height="360px", display=DisplayTarget.MANUAL
    )
    chart.animate(data)
    chart.animate(
        Config(
            {
                "channels": {
                    "x": {
                        "attach": ["Country"]
                        #"label": "Decade",  # List of data columns to attach to the x-axis
                    },
                    "y": {
                        #"title": "Average",
                        "attach": ["LCOE (USD/MWh)"]  # List of data columns to attach to the y-axis
                    },
                },
                "legend": "label",
                "title" : "LCOE"
            }
        )
    )

    '''
            {
                "x": "Decade",
                "y": "Average",
                #"dividedBy": "Month Name",
                "title": "CO2 Concentration",
                "axistitle"
            }
            
            }
        ),
        Style(
            {
                "plot": {
                    "marker": {
                        "label": {
                            "fontSize": 6,
                            "orientation": "vertical",
                            "angle": -3.14,
                        }
                    }
                }
            }
        ),
    )

    '''

    ''' GENERATION OF HTML FILE '''

    file_name = "generated_html.html"  # Change this to your desired file name

    half1 = """<html>
    <head>
        <meta charset="utf-8">
        <title>Vizzu Chart</title>
    </head>
    <body>
    """

    half2 = """</body>
    </html>"""

    html = half1 + chart._repr_html_() + half2

    #Open the file in write mode and write the HTML content
    with open(file_name, "w") as html_file:
        html_file.write(html)
    return file_name



def capture_animation_frames(html_file, output_directory):
    ''' CAPTURES FRAMES OF ANIMATION '''
    # Configure Chrome options for headless mode and set the webdriver executable path
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--start-maximized")
    chrome_options.binary_location = r"C:\Program Files\...\chrome.exe"  # Replace with your Chrome executable path
    driver_path = r"C:\Users\...\chromedriver.exe"  # Replace with your Chromedriver executable path
    driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=chrome_options)

    # Load the HTML animation file
    driver.get(f'file://{os.path.abspath(html_file)}')

    # Adjust the viewport size as needed
    driver.set_window_size(700, 400)
    frames = []
    frame_number = 1

    while frame_number <= 100:  # Capture 100 frames (adjust as needed)
        # Capture a screenshot of the current page
        screenshot = driver.get_screenshot_as_png()

        # Save the screenshot as an image file
        image_file = os.path.join(output_directory, f'frame_{frame_number:03d}.png')
        with open(image_file, 'wb') as img:
            img.write(screenshot)
        frames.append(image_file)

        # Wait for a short duration (adjust as needed)
        time.sleep(0.1)  # Wait for 100 milliseconds

        frame_number += 1

    driver.quit()
    return frames

def create_gif(frames, output_gif):
    ''' CREATES GIF FROM ALL FRAMES'''
    with imageio.get_writer(output_gif, mode='I', duration=0.1) as writer:
        for frame in frames:
            image = imageio.imread(frame)
            writer.append_data(image)

def main():
    
    html_file = ChartCreation()
    output_directory = 'frames'
    output_gif = 'animation.gif'

    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory)

    capture_animation_frames(html_file, output_directory)
    create_gif(sorted([os.path.join(output_directory, filename) for filename in os.listdir(output_directory)]), output_gif)

    
    print(f'GIF animation saved as {output_gif}')

if __name__ == "__main__":
    main()