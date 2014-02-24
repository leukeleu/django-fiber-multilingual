(function($) {

Fiber.enhance_textarea = function(textarea, auto_height) {

	if (! CKEDITOR || ! CKEDITOR.replace) {
		// ckeditor not installed
		return;
	}

	if (window.CKEDITOR_CONFIG_STYLES_SET) {
		if (!CKEDITOR.stylesSet.get('config_styles_set')) {
			CKEDITOR.stylesSet.add('config_styles_set', window.CKEDITOR_CONFIG_STYLES_SET);
		}
	}

	window.CKEDITOR_CONFIG_TOOLBAR = window.CKEDITOR_CONFIG_TOOLBAR || [
		['Format'],
		window.CKEDITOR_CONFIG_STYLES_SET ? ['Styles'] : '-',
		['Bold','Italic'],
		['NumberedList','BulletedList','Outdent','Indent'],
		['fPageLink','fFileLink','fImageLink','fCustomLink','fUnlink'],
		['fImage','Table'],
		['PasteText','PasteFromWord','RemoveFormat'],
		['Maximize'],
		['Source']
	];

	if (auto_height) {
		CKEDITOR.config.height = window.innerHeight - (($('.ui-dialog').height() - $(textarea).height()) + 140);
	}

	var fiber_data = get_fiber_data();
	language_code = fiber_data.language_code;

	CKEDITOR.replace(textarea, {
		skin: 'moono',
		language: language_code,
		extraPlugins: 'fpagelink,ffilelink,fimagelink,fcustomlink,funlink,fimage,table,tabletools',
		removePlugins: 'scayt,language,menubutton,forms,image,link',
		extraAllowedContent: 'a[*]{*}(*);img[*]{*}(*);iframe[*];object[*];param[*];embed[*]',
		toolbar: window.CKEDITOR_CONFIG_TOOLBAR,
		format_tags: window.CKEDITOR_CONFIG_FORMAT_TAGS || 'p;h2;h3;h4',
		stylesSet: window.CKEDITOR_CONFIG_STYLES_SET || null,
		toolbarCanCollapse: false,
		resize_maxWidth: 610,
		baseFloatZIndex: 1100
	});
};

Fiber.remove_textarea = function(textarea) {
	if (CKEDITOR.instances && textarea.id in CKEDITOR.instances) {
		CKEDITOR.instances[textarea.id].destroy(false);
	}
};

function extend_CKEditor() {

	if (! CKEDITOR || ! CKEDITOR.plugins) {
		return;
	}

	// fPageLink
	var fpagelinkCmd = {
		canUndo: false,
		exec: function(editor) {

			// show page select dialog
			var page_select_dialog = new Fiber.PageSelectDialog();

			page_select_dialog.action_click = function() {
				// delete any existing links on the selected text
				editor.document.$.execCommand('unlink', false, null);

				// create a new link
				editor.focus();
				var selection = editor.getSelection(); // need to do this to 'initialize'
				var style = new CKEDITOR.style({
					element: 'a',
					attributes: {
						'href': page_select_dialog.selected_url
					}
				});
				style.type = CKEDITOR.STYLE_INLINE;
				style.apply(editor.document);

				this.destroy();
			};
		}
	};

	// register plugin 'fpagelink'
	CKEDITOR.plugins.add('fpagelink', {
		init: function(editor) {
			editor.addCommand('fpagelink', fpagelinkCmd);
			editor.ui.addButton('fPageLink', {
				label: gettext('Link to a Page in This Site'),
				command: 'fpagelink',
				icon: get_static_url() + 'fiber/images/ckeditor/icon-pagelink.png'
			});
		}
	});

	// fFileLink
	var ffilelinkCmd = {
		canUndo: false,
		exec: function(editor) {

			// show file select dialog
			var file_select_dialog = new Fiber.FileSelectDialog();

			file_select_dialog.action_click = function() {
				var row = file_select_dialog.get_selected_row();
				var selected_file_path = row.file_url;

				// delete any existing links on the selected text
				editor.document.$.execCommand('unlink', false, null);

				// create a new link
				editor.focus();
				var selection = editor.getSelection();
				var style = new CKEDITOR.style({
					element: 'a',
					attributes: {
						'href': selected_file_path
					}
				});
				style.type = CKEDITOR.STYLE_INLINE;
				style.apply(editor.document);

				this.destroy();
			};
		}
	};

	// register plugin 'ffilelink'
	CKEDITOR.plugins.add('ffilelink', {
		init: function(editor) {
			editor.addCommand('ffilelink', ffilelinkCmd);
			editor.ui.addButton('fFileLink', {
				label: gettext('Link to a File in This Site'),
				command: 'ffilelink',
				icon: get_static_url() + 'fiber/images/ckeditor/icon-filelink.png'
			});
		}
	});

	// fImageLink
	var fimagelinkCmd = {
		canUndo: false,
		exec: function(editor) {

			// show image select dialog
			var image_select_dialog = new Fiber.ImageSelectDialog();

			image_select_dialog.action_click = function() {
				var row = image_select_dialog.get_selected_row();
				var selected_image_path = row.image_url;

				// delete any existing links on the selected text
				editor.document.$.execCommand('unlink', false, null);

				// create a new link
				editor.focus();
				var selection = editor.getSelection();
				var style = new CKEDITOR.style({
					element: 'a',
					attributes: {
						'href': selected_image_path
					}
				});
				style.type = CKEDITOR.STYLE_INLINE;
				style.apply(editor.document);

				this.destroy();
			};
		}
	};

	// register plugin 'fimagelink'
	CKEDITOR.plugins.add('fimagelink', {
		init: function(editor) {
			editor.addCommand('fimagelink', fimagelinkCmd);
			editor.ui.addButton('fImageLink', {
				label: gettext('Link to an Image in This Site'),
				command: 'fimagelink',
				icon: get_static_url() + 'fiber/images/ckeditor/icon-imagelink.png'
			});
		}
	});

	// fCustomLink
	var fcustomlinkCmd = {
		canUndo: false,
		exec: function(editor) {

			// prompt for custom link - TODO: create custom jQuery UI dialog for this
			var custom_link = window.prompt(gettext('Please Enter a Link'), 'http://');

			// delete any existing links on the selected text
			editor.document.$.execCommand('unlink', false, null);

			// create a new link
			editor.focus();
			var selection = editor.getSelection();
			var style = new CKEDITOR.style({
				element: 'a',
				attributes: {
					'href': custom_link
				}
			});
			style.type = CKEDITOR.STYLE_INLINE;
			style.apply(editor.document);
		}
	};

	// register plugin 'fcustomlink'
	CKEDITOR.plugins.add('fcustomlink', {
		init: function(editor) {
			editor.addCommand('fcustomlink', fcustomlinkCmd);
			editor.ui.addButton('fCustomLink', {
				label: gettext('Custom Link'),
				command: 'fcustomlink',
				icon: get_static_url() + 'fiber/images/ckeditor/icon-customlink.png'
			});
		}
	});

	// fUnlink
	var funlinkCmd = {
		canUndo: false,
		exec: function(editor) {
			// delete any existing links on the selected text
			editor.document.$.execCommand('unlink', false, null);
		}
	};

	// register plugin 'funlink'
	CKEDITOR.plugins.add('funlink', {
		init: function(editor) {
			editor.addCommand('funlink', funlinkCmd);
			editor.ui.addButton('fUnlink', {
				label: gettext('Unlink'),
				command: 'funlink',
				icon: get_static_url() + 'fiber/images/ckeditor/icon-unlink.png'
			});
		}
	});

	// fImage
	var fimageCmd = {
		canUndo: false,
		exec: function(editor) {

			// show image select dialog
			var image_select_dialog = new Fiber.ImageSelectDialog();

			image_select_dialog.action_click = function() {
				var selected_image_path = $(this.uiDialog.find('tr.selected td'));
				selected_image_path =$(selected_image_path[0]).text();
				var selected_image_title = '';

				// create image element, and insert it
				var imageElement = CKEDITOR.dom.element.createFromHtml('<img src="' + selected_image_path + '" title="' + CKEDITOR.tools.htmlEncode(selected_image_title) + '" />');
				editor.insertElement(imageElement);

				this.destroy();
			};
		}
	};

	// register plugin 'fimage'
	CKEDITOR.plugins.add('fimage', {
		init: function(editor) {
			editor.addCommand('fimage', fimageCmd);
			editor.ui.addButton('fImage', {
				label: gettext('Image'),
				command: 'fimage',
				icon: get_static_url() + 'fiber/images/ckeditor/icon-image.png'
			});
		}
	});
}

function get_fiber_data() {
	return $.parseJSON($('body').dataset('fiber-data'));
}

var static_url = null;

function get_static_url() {
	if (! static_url) {
		static_url = get_fiber_data().static_url;
	}

	return static_url;
}

extend_CKEditor();

})(fiber_jQuery);
