import os
import random
import shutil
import string
import threading
import time

from playwright.sync_api import sync_playwright

from m import solver_spiral


class CreateOutlook(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def click_audio(self):
        self.frame.wait_for_selector("#audio_play", timeout=0)
        self.frame.click("#audio_play")
        time.sleep(3)

    def get_frame(self):
        self.page.wait_for_selector('#fc-iframe-wrap', timeout=4000)
        frame_element_handle = self.page.query_selector('#fc-iframe-wrap')
        self.frame_parent = frame_element_handle.content_frame()

        self.frame_parent.wait_for_selector('#CaptchaFrame', timeout=4000)
        frame_element_handle = self.frame_parent.query_selector('#CaptchaFrame')
        self.frame_child = frame_element_handle.content_frame()

    def click_custom(self, page, selector):
        for i in range(5):
            try:
                elm = page.query_selector(selector)
                if elm != None:
                    time.sleep(1)
                    elm.click()
                    break
            except:
                pass
            finally:
                time.sleep(1)

    def fill_custom(self, page, selector, value):
        for i in range(20):
            try:
                elm = page.query_selector(selector)
                if elm != None:
                    time.sleep(1)
                    elm.fill(value)
                    break
            except:
                pass
            finally:
                time.sleep(1)

    def get_image(self):
        name = "".join(random.choices(string.digits + string.ascii_uppercase, k=7))
        # set folder to store images
        self.image_path = './t/' + name + '/'
        image_element = self.frame_child.query_selector(
            "[aria-label='Visual challenge. Audio challenge is available below. Compatible with screen reader software. Image 1. ']")
        new_name = self.image_path + name + str(1) + '.png'
        image_element.screenshot(path=new_name)
        for i in range(2, 7):
            image_element = self.frame_child.query_selector(f"[aria-label='Image {i}.']")
            new_name = self.image_path + name + str(i) + '.png'
            image_element.screenshot(path=new_name)

    def click_image(self, imageth):
        if imageth == 1:
            self.frame_child.query_selector(
                'css=[aria-label="Visual challenge. Audio challenge is available below. Compatible with screen reader software. Image 1. "]').click()
        else:
            self.frame_child.query_selector(f'css=[aria-label="Image {imageth}."]').click()

    def save_token(self, token):
        with open("token.txt", 'a') as f:
            f.write(token + '\n')

    def run_create(self, p, ip=None, port=None):
        # init browser
        browser = p.firefox.launch(
            headless=False,
        )
        self.context = browser.new_context()
        self.page = self.context.new_page()
        self.page.set_default_timeout(timeout=40000)
        try:
            self.page.goto(
                "https://iframe-auth.arkoselabs.com/2F1CD804-FE45-F12B-9723-240962EBA6F8/index.html?data=oX%2FZ5mB7c4XKte67%2BV1URA%3D%3D.%2FG3TfSE2nSppiiPEk2nx1NYKXozQcDL02iSVBi4guyYCZ47VR4dcBLwUhlq6W6of1H1ZX1s1T56IVoiZrL8C7xgyiJ9mBTNP4Hky4XCWN1lJoAOG3zzXKP4OA73%2BABcZcpZMTy%2B1DfYZUN7y3dz5ZmF5kfI%3D&mkt=en-US")
        except Exception as e:
            print('[Error] ', e)
        # verify button
        timeCounter = 15
        while timeCounter > 0:
            try:
                self.get_frame()
                self.frame_child.wait_for_selector('#home_children_button')
                break
            except Exception as e:
                pass
            finally:
                timeCounter -= 1
                time.sleep(1)
        print("Click button")
        self.click_custom(self.frame_child, '#home_children_button')
        try:
            while True:
                print("Get frame")
                self.get_frame()
                # self.click_custom(self.frame_parent, '.fc_meta_reload_btn')
                try:
                    print("Get image")
                    self.get_image()
                except:
                    # delete image path
                    if os.path.isdir(self.image_path):
                        shutil.rmtree(self.image_path)
                    break
                # solve captcha
                imageth = solver_spiral.solver(self.image_path)
                # delete image path
                shutil.rmtree(self.image_path)
                # click image
                self.click_image(imageth)
                print('Result: ', imageth)
                time.sleep(2)
                # victory
            # get verification token
            verify_token = self.page.query_selector('#verification-token').get_attribute('value')
            print(verify_token)
            # save token
            self.save_token(verify_token)
        except:
            pass
        finally:
            browser.close()

    def run(self):
        try:
            with sync_playwright() as playwright:
                ip, port = "", ""
                self.run_create(playwright, ip, port)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    n_token = int(input("How tokens do u want to create? "))
    for i in range(500):
        threads = []
        for k in range(n_token):
            outlook = CreateOutlook()
            threads.append(outlook)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        break