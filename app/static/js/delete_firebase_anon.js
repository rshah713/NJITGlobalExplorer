/**
 * Batch-delete Firebase Anonymous Users
 */
function deleteAccounts() {
    function next() {
        var threeDotsXPath = '//*[@id="auth-users-table"]/tbody/tr[1]/td[6]/edit-account-menu/button/span[3]';

        var threeDotsElement = document.evaluate(threeDotsXPath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (threeDotsElement) {
            threeDotsElement.click();
            setTimeout(function() {
                var buttons = document.getElementsByTagName('button');
                var deleteAccountButton = null;
                for (var j = 0; j < buttons.length; j++) {
                    if (buttons[j].textContent.trim() == 'Delete account') {
                        deleteAccountButton = buttons[j];
                        break;
                    }
                }
                if (deleteAccountButton) {
                    deleteAccountButton.click();
                    setTimeout(function() {
                        var buttons = document.querySelectorAll('button');
                        var deleteButton = Array.from(buttons).find(button => button.textContent.trim() === 'Delete' && button.classList.contains('confirm-button'));
                        if (deleteButton) {
                            deleteButton.click();
                            setTimeout(next, 1000);  // wait for 2 seconds before moving to the next row
                        }
                    }, 500);  // wait for 1 second before clicking "Delete"
                }
            }, 500);  // wait for 1 second before clicking "Delete Account"
        } else {
            console.log('No more accounts to delete.');
        }
    }
    next();
}

deleteAccounts();