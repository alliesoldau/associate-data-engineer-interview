class CreateCounselors < ActiveRecord::Migration[6.1]
  def change
    create_table :counselors do |t|
      t.string :name
    end
  end
end
