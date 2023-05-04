class CreateTransfers < ActiveRecord::Migration[6.1]
  def change
    create_table :transfers do |t|
      t.integer :contact_id
      t.integer :counselor_id
      t.timestamp :datetime
    end
  end
end
