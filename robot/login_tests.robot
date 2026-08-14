*** Settings ***
Documentation     Robot Framework demo re-implementing the core login scenarios
...               from tests/test_login.py, to demonstrate keyword-driven test
...               automation alongside the Python/pytest suite in this repo.
Library           SeleniumLibrary
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${URL}                https://www.saucedemo.com/
${BROWSER}             headlesschrome
${STANDARD_USER}       standard_user
${LOCKED_OUT_USER}     locked_out_user
${PASSWORD}            secret_sauce

*** Test Cases ***
Successful Login Shows Inventory Page
    Input Text          id:user-name    ${STANDARD_USER}
    Input Text          id:password     ${PASSWORD}
    Click Button        id:login-button
    Element Text Should Be    class:title    Products

Locked Out User Sees Error Message
    Go To    ${URL}
    Input Text          id:user-name    ${LOCKED_OUT_USER}
    Input Text          id:password     ${PASSWORD}
    Click Button        id:login-button
    Element Should Contain    css:[data-test='error']    locked out

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
