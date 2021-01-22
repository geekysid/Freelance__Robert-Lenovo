#!/usr/local/bin/python3


# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#   Name: Siddhant Shah                             #
#   Date: 20/10/2020                                #
#   Desc: SCRAPER FOR LENOVO HTML                   #
#   Email: siddhant.shah.1986@gmail.com             #
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, os, sys


# global variables
DATA = {}
CONFIG_DATA = {}


# just fro decoration
def intro_deco():
	print("\n\n")
	print("\t", '#'*40)
	print("\t", "#                                      #")
	print("\t", "#        SCRAPER FOR LENOVO HTML       #")
	print("\t", "#           By: SIDDHANT SHAH          #")
	print("\t", "#             Dt: 21-10-2020           #")
	print("\t", "#     siddhant.shah.1986@gmail.com     #")
	print("\t", "#   **Just for Educational Purpose**   #")
	print("\t", "#                                      #")
	print("\t", '#'*40)
	print()


# getting information from config file
def initializer():
	global CONFIG_DATA

	if os.path.exists(f'{PATH}config.json'):
		with open (f'{PATH}config.json', 'r') as r:
			CONFIG_DATA = json.load(r)

		# print(CONFIG_DATA['features'])
		# print(CONFIG_DATA['specifications'])


# Setting up webdriver
def get_browser(headless=False):

	# linux
	if sys.platform == "linux" or sys.platform == "linux2":
		pass
	# OS X
	elif sys.platform == "darwin":
		pathToChromeDriver = f"{PATH}chromedriver"

	# Windows
	elif sys.platform == "win32":
		pathToChromeDriver = f'{PATH}chromedriver'

	else:
		print(sys.platform)

	chrome_options = Options()

	# giving a higher resolution to headless browser so that click operation works
	if headless:
		chrome_options.headless = headless
	else:
		chrome_options.add_argument('--window-size=1920,1080')
		chrome_options.add_argument("--start-maximized")

	browser = webdriver.Chrome(executable_path = pathToChromeDriver, options=chrome_options)

	return browser


# getting headinng section from a model
def get_heading_section(browser):
	global DATA
	print('  [+] Fetching Header Data')
	browser.get(CONFIG_DATA['features'])

	try:
		WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.CLASS_NAME,'desktopHeader')))

		heading = browser.find_element_by_xpath('//h1[contains(@class, "desktopHeader")]').text.replace('\"', "").replace('\'', "")
		subHeading = browser.find_element_by_xpath('//h3[contains(@class, "heroSubHeader")]').text
		pro_desc_body = browser.find_element_by_xpath('//div[contains(@class, "hero-productDescription-body")]').get_attribute('innerHTML')
		product_img_url = browser.find_element_by_xpath('//div[contains(@class, "hero-pc-img")]').find_elements_by_tag_name('img')[-1].get_attribute('src')

		DATA['heading'] = {
			'title': heading,
			'subHeading': subHeading,
			'description': pro_desc_body,
			'cover_img': product_img_url
		}

	except Exception as error:
		print(f'Exception @ get_heading_section() => {error}')


# getting Features for a model
def get_features_section(browser):
	global DATA
	print('  [+] Fetching Features Data')

	try:
		WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.ID,'tab-features')))
		time.sleep(10)
		# geeting feature section
		feature_element = browser.find_element_by_xpath('//*[@id="tab-features"]')
		sections = feature_element.find_elements_by_tag_name('section')

		section_count = 0
		DATA['features'] = {}

		for section in sections:
			DATA['features'][section_count] = {}
			section_main_div = section.find_element_by_xpath('//div[contains(@class, "tabbedBrowse-features-featureText")]')

			valid_heading_index = []
			# getting headings
			headings = section.find_elements_by_xpath('//h2[contains(@class, "tabbedBrowse-features-featureHeading")]')
			headings = section.find_elements_by_tag_name('h2')
			heading_count = 0

			for heading in headings:
				if heading.text:
					DATA['features'][section_count][f'heading_{heading_count}'] = heading.text
					valid_heading_index.append(heading_count)
				heading_count += 1

			# getting descriptions
			descriptions = section.find_elements_by_class_name('tabbedBrowse-features-featureText')
			description_count = 0

			for index in valid_heading_index:
				DATA['features'][section_count][f'description_{index}'] = descriptions[index].text

			# getting section image
			section_img_url = section.find_element_by_tag_name('img').get_attribute('data-original')
			try:
				section_img_url = 'https://www.lenovo.com/'+section_img_url
			except:
				section_img_url = section.find_element_by_tag_name('img').get_attribute('src')
			# section_img_url = section.find_element_by_xpath('//img[contains(@class, "lazyLoadAfterDOMInteractive")]').get_attribute('src')
			# print(section_img_url)

			DATA['features'][section_count]['img'] = section_img_url

			section_count += 1

	except Exception as error:
		# print(f'Exception @ get_features_section() => {error}')
		pass
		# input()


# getting Specifications for a model
def get_specifications(browser):
	global DATA
	print('  [+] Fetching Specifiations Data')
	browser.get(CONFIG_DATA['specifications'])
	DATA['specifications'] = {
		'head':{},
		'specs': {}
	}

	try:

		WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.ID,'modeldetail')))
		spec_table = browser.find_element_by_id('modeldetail').find_elements_by_tag_name('table')[0]

		header_row = spec_table.find_element_by_tag_name('thead').find_elements_by_tag_name('th')
		DATA['specifications']['head'][header_row[0].text] = header_row[1].text

		spec_rows = spec_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

		row_count = 0

		for spec_row in spec_rows:
			title = spec_row.find_elements_by_tag_name('td')[0].text
			desc = spec_row.find_elements_by_tag_name('td')[1].text

			DATA['specifications']['specs'][row_count] = {
				'title': title,
				'desc': desc
			}
			row_count += 1

	except Exception as error:
		print(f'Exception @ get_specifications() => {error}')


# creating string that represent html part of HEADING
def creater_heading_html_string():
	html_heading = '''
						<!-- HEADING start -->
							<table width="100%" style="background-color: !!COVER_BACKGROUND_COLOR!!">
								<tr>
									<td align="center">
										<table width="70%" style="color: !!COVER_TEXT_COLOR!!">
											<tr>
												<td width="60%">
													<h1 style="text-align: left">!!HEADING!!</h1>
													<div>
														<span style="font-size:115%;">!!SUB-HEADING!!</span>
														<br />
														<span style="font-size:70%">!!DESCRIPTION!!</span>
													</div>
													<p>
														&nbsp;
													</p>
												</td>
												<td width="40%" style="text-align: center;">
														<img src="!!IMAGE_SRC!!" style="" width="300"/>
												</td>
											</tr>
										</table>
									</td>
								</tr>
							</table>
						<!-- HEADING end -->'''

	html_heading = html_heading.replace('!!HEADING!!',
						DATA['heading']['title']). replace('!!SUB-HEADING!!',
						DATA['heading']['subHeading']).replace('!!DESCRIPTION!!',
						DATA['heading']['description']).replace('!!IMAGE_SRC!!',
						DATA['heading']['cover_img']).replace('!!COVER_BACKGROUND_COLOR!!',
						CONFIG_DATA['cover_background_color']).replace('!!COVER_TEXT_COLOR!!',
						CONFIG_DATA['cover_text_color'])

	return html_heading


# creating string that represent html part of HEADING
def creater_features_html_string():

	html_features = '''
					<!-- FEATURES start -->
					<table width="70%">
						<!-- HEADING -->
						<tr>
							<td colspan="2">
								<h2 style="text-align: left; font-weight; text-decoration: underline;">Features</h2>
							</td>
						</tr>
						!!SECTION!!
					</table>
					<!-- FEATURES end -->'''

	sections_1 = '''
				<tr>
					<td width="50%">
						!!SECTION_ROW!!
					</td>
					<td width="50%" style="text-align: center;">
						<img src="!!SECTION_IMG!!" style="" width="!!FEATURES_IMAGES_WIDTH!!"/>
					</td>
				</tr>
				<tr>
					<td style="width:50%">
						<br />
					</td>
					<td style="width:50%">
						<br />
					</td>
				</tr>'''
	sections_2 = '''
				<tr>
					<td width="50%" style="text-align: center;">
						<img src="!!SECTION_IMG!!" style="" width="!!FEATURES_IMAGES_WIDTH!!"/>
					</td>
					<td width="50%">
						!!SECTION_ROW!!
					</td>
				</tr>
				<tr>
					<td style="width:50%">
						<br />
					</td>
					<td style="width:50%">
						<br />
					</td>
				</tr>'''

	features = DATA['features']
	sections = ''

	for i in range(len(features.keys())):
		if 'img' in features[i].keys():
			rows = ''
			for j in range(len(features[i].keys())):
				if f'heading_{j}' in features[i].keys():
					heading = features[i][f'heading_{j}']
					desc = features[i][f'description_{j}']

					rows += '''<p>
								<div>
									<span style="font-size:105%; font-weight:lighter">!!HEADING!!</span>
									<br />
									<span style="font-size:75%">!!DESC!!</span>
								</div>
							</p>'''.replace('!!HEADING!!', heading).replace('!!DESC!!', desc)

				else:
					continue

			img = features[i]['img']

			if i % 2 == 0:
				sections += sections_1.replace('!!SECTION_ROW!!', rows).replace("!!SECTION_IMG!!", img).replace('!!FEATURES_IMAGES_WIDTH!!', CONFIG_DATA['features_images_width'])
			else:
				sections += sections_2.replace('!!SECTION_ROW!!', rows).replace("!!SECTION_IMG!!", img).replace('!!FEATURES_IMAGES_WIDTH!!', CONFIG_DATA['features_images_width'])

	return html_features.replace('!!SECTION!!', sections)


# creating string that represent html part of specification
def creater_specification_html_string():
	html_specifictaions = '''
					<!-- SPECIFICATIONS starts -->
						<table width="70%">
							<!-- HEADING -->
							<tr style="height: 150%;">
								<td colspan="3">
									<h2 style="text-align: left; font-weight; text-decoration: underline;">Specifications</h2>
								</td>
							</tr>

							<tr>
								<td colspan="3">
									<table style="text-align: center; width:100%; border: 1px solid grey; font-size: 85%">
										<thead>
											!!THEAD!!
										</thead>
										<tbody>
											!!TBODY!!
										</tbody>
									</table>
								</td>
							</tr>
						</table>
					<!-- SPECIFICATIONS end -->'''

	specs = DATA['specifications']['specs']
	rows = ''

	for i in range(len(specs.keys())):
		title = specs[i]['title']
		desc = specs[i]['desc']
		if i % 2 == 0:
			row = '''<tr style="background-color: rgb(255, 255, 255); line-height: 200%;">
						<td style="background-color: rgb(210, 210, 210);">!!TITLE!!</td>
						<td style="background-color: rgb(210, 210, 210);">!!DESC!!</td>
					</tr>
				'''
		else:
			row = '''
					<tr style="line-height: 200%;">
						<td>!!TITLE!!</td>
						<td>!!DESC!!</td>
					</tr>
				'''
		rows += row.replace('!!TITLE!!', title).replace('!!DESC!!', desc)

	header = f'<tr><th style="width:25%; color: white; background-color: black;">Model</th><th style="width:75%; color: white; background-color: black;">{DATA["specifications"]["head"]["Model"]}</th></tr>'
	return html_specifictaions.replace('!!THEAD!!', header).replace('!!TBODY!!', rows)


# generating HTML String
def generate_html_string():
	print('  [+] Generating HTML String')
	html_start = '''<div style="color:#444; font-size: 18px; font-family: 'Source Sans Pro', sans-serif;"><table><tr><td align="center">'''
	html_end = '''</td></tr></table></div><br /><br /><br />'''

	html_structure =  html_start + creater_heading_html_string() + '<br /><br />' + creater_features_html_string() + '<br /><br />' + creater_specification_html_string() + html_end

	html_file = DATA["heading"]["title"].replace(" ", "_").replace("\"", "")+'.html'
	with open(f'{PATH}{html_file}', 'w', encoding="utf-8") as w:
		w.write(html_structure)

	print(f'  [+] HTML Template generated and saved as {html_file}')


# getting required data from website
def get_required_data(browser):
	get_heading_section(browser)
	get_features_section(browser)
	get_specifications(browser)
	# print(json.dumps(DATA, indent=4))
	# input()


# executing script only if its not imported
if __name__ == '__main__':

    PATH = f'{os.getcwd()}/'
    # print(PATH)
    # PATH = f'C:\\Robert__\\'
    # print(PATH)

    intro_deco()
    initializer()
    browser = get_browser(headless=False)
    get_required_data(browser)
    browser.quit()
    generate_html_string()


